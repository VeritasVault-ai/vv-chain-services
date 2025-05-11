import { BigInt, Bytes, ethereum, Address } from '@graphprotocol/graph-ts';

// Import the generated contract bindings
import {
  Deposit as DepositEvent,
  Withdrawal as WithdrawalEvent,
  PriceUpdate as PriceUpdateEvent
} from '../generated/VaultContract/VaultContract';

// Import the generated schema types
import { Vault, Transaction, PriceUpdate as PriceUpdateEntity } from '../generated/schema';

export function handleDeposit(event: DepositEvent): void {
  // Extract data from the EVM event
  let vaultId = event.params.from.toHexString();
  let amount = event.params.amount;
  
  // Load or create vault
  let vault = Vault.load(vaultId);
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.params.from;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
  }
  
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

export function handleWithdrawal(event: WithdrawalEvent): void {
  // Extract data from the EVM event
  let vaultId = event.params.to.toHexString();
  let amount = event.params.amount;
  
  // Load or create vault
  let vault = Vault.load(vaultId);
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.params.to;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
  }
  
  // Update vault data
  // Validate withdrawal amount to prevent negative balances
  if (vault.totalValue.ge(amount)) {
    vault.totalValue = vault.totalValue.minus(amount);
  } else {
    // Handle insufficient funds case - either log an error or set to zero
    vault.totalValue = BigInt.fromI32(0);
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

export function handlePriceUpdate(event: PriceUpdateEvent): void {
  // Extract data from the EVM event
  let vaultId = event.transaction.from.toHexString();
  let asset = event.params.asset;
  let price = event.params.price;
  
  // Load or create vault
  let vault = Vault.load(vaultId);
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.transaction.from;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
    vault.updatedAt = event.block.timestamp;
    vault.save();
  }
  
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