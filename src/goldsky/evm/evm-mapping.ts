import { BigInt, Bytes, ethereum, Address } from '@graphprotocol/graph-ts';

 // Import the generated contract bindings
 import {
   Deposit as DepositEvent,
   Withdrawal as WithdrawalEvent,
   PriceUpdate as PriceUpdateEvent
 } from '../generated/VaultContract/VaultContract';

 // Import the generated schema entities
 import { Vault, Transaction, PriceUpdate as PriceUpdateEntity } from '../generated/schema';

 // Constants
 const DEFAULT_TOTAL_VALUE = 0;
/**
 * Helper function to get an existing vault or create a new one with default values.
 */
function getOrCreateVault(id: string, owner: Bytes, timestamp: BigInt): Vault {
  let vault = Vault.load(id);
  if (!vault) {
    vault = new Vault(id);
    vault.owner = owner;
    vault.totalValue = BigInt.fromI32(DEFAULT_TOTAL_VALUE);
    vault.createdAt = timestamp;
    vault.updatedAt = timestamp;
  }
  return vault;
}

/**
 * Handles a deposit event by updating the corresponding vault's total value and recording the deposit transaction.
 *
 * If the vault does not exist, it is created and initialized with the depositor as the owner.
 */
export function handleDeposit(event: DepositEvent): void {
  // Extract data from the EVM event
  let vaultId = event.params.from.toHexString();
  let amount = event.params.amount;
  
  // Get or create vault
  let vault = getOrCreateVault(vaultId, event.params.from, event.block.timestamp);
  
  // Update vault data
  vault.totalValue = vault.totalValue.plus(amount);
  vault.updatedAt = event.block.timestamp;
  vault.save();
  
  // Create transaction record
  let transactionId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let transaction = new Transaction(transactionId);
  transaction.vault = vaultId;
  transaction.from = event.params.from;
  transaction.to = null;
  transaction.amount = amount;
  transaction.timestamp = event.block.timestamp;
  transaction.transactionHash = event.transaction.hash;
  transaction.blockNumber = event.block.number;
  transaction.type = 'deposit';
  transaction.save();
}

/**
 * Handles a Withdrawal event by updating the corresponding Vault entity and recording the withdrawal as a Transaction.
 *
 * If the vault does not exist, it is created. The vault's total value is decreased by the withdrawal amount, or set to zero if insufficient funds are available. A Transaction entity is created to record the withdrawal details.
 *
 * @remark If the withdrawal amount exceeds the vault's total value, the vault's total value is set to zero rather than reverting or throwing an error.
 */
export function handleWithdrawal(event: WithdrawalEvent): void {
  // Extract data from the EVM event
  let vaultId = event.params.to.toHexString();
  let amount = event.params.amount;
  
  // Get or create vault
  let vault = getOrCreateVault(vaultId, event.params.to, event.block.timestamp);
  
  // Withdrawal: ensure we don't go negative
  if (vault.totalValue.ge(event.params.amount)) {
    vault.totalValue = vault.totalValue.minus(event.params.amount);
  } else {
    // Handle insufficient funds case – here we zero out, but you may want to log or revert
    vault.totalValue = BigInt.fromI32(DEFAULT_TOTAL_VALUE);
  }
  vault.updatedAt = event.block.timestamp;
  vault.save();
  
  // Create transaction record
  let transactionId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let transaction = new Transaction(transactionId);
  transaction.vault = vaultId;
  transaction.from = null;
  transaction.to = event.params.to;
  transaction.amount = amount;
  transaction.timestamp = event.block.timestamp;
  transaction.transactionHash = event.transaction.hash;
  transaction.blockNumber = event.block.number;
  transaction.type = 'withdrawal';
  transaction.save();
}

/**
 * Handles a PriceUpdate event by recording the updated asset price for a vault.
 *
 * Loads or creates the associated Vault entity, then creates a new PriceUpdate entity with the asset, price, and event metadata.
 */
export function handlePriceUpdate(event: PriceUpdateEvent): void {
  // Extract data from the EVM event
  let vaultId = event.transaction.from.toHexString();
  let asset = event.params.asset;
  let price = event.params.price;
  
  // Get or create vault
  let vault = getOrCreateVault(vaultId, event.transaction.from, event.block.timestamp);
  vault.updatedAt = event.block.timestamp;
  vault.save();
  
  // Create price update record
  let priceUpdateId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let priceUpdate = new PriceUpdateEntity(priceUpdateId);
  priceUpdate.vault = vaultId;
  priceUpdate.asset = asset;
  priceUpdate.price = price;
  priceUpdate.timestamp = event.block.timestamp;
  priceUpdate.transactionHash = event.transaction.hash;
  priceUpdate.blockNumber = event.block.number;
  priceUpdate.save();
}
