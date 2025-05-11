import { BigInt } from '@graphprotocol/graph-ts';
import { Vault, Transaction, PriceUpdate } from '../generated/schema';

export function handleDeposit(event: any): void {
  // Extract data from the Tezos event
  let vaultId = event.parameters.from;
  let amount = BigInt.fromString(event.parameters.amount);
  
  // Load or create vault
  let vault = Vault.load(vaultId);
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = vaultId;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = BigInt.fromString(event.timestamp.toString());
  }
  
  // Update vault data
  vault.totalValue = vault.totalValue.plus(amount);
  vault.updatedAt = BigInt.fromString(event.timestamp.toString());
  vault.save();
  
  // Create transaction record
  let transactionId = event.operation.hash + '-' + event.id;
  let transaction = new Transaction(transactionId);
  transaction.vault = vaultId;
  transaction.from = event.parameters.from;
  transaction.to = null;
  transaction.amount = amount;
  transaction.timestamp = BigInt.fromString(event.timestamp.toString());
  transaction.operationHash = event.operation.hash;
  transaction.blockLevel = BigInt.fromString(event.block.level.toString());
  transaction.type = 'deposit';
  transaction.save();
}

export function handleWithdrawal(event: any): void {
  // Extract data from the Tezos event
  let vaultId = event.parameters.to;
  let amount = BigInt.fromString(event.parameters.amount);
  
  // Load or create vault
  let vault = Vault.load(vaultId);
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = vaultId;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = BigInt.fromString(event.timestamp.toString());
  }
  
  // Update vault data
  vault.totalValue = vault.totalValue.minus(amount);
  vault.updatedAt = BigInt.fromString(event.timestamp.toString());
  vault.save();
  
  // Create transaction record
  let transactionId = event.operation.hash + '-' + event.id;
  let transaction = new Transaction(transactionId);
  transaction.vault = vaultId;
  transaction.from = null;
  transaction.to = event.parameters.to;
  transaction.amount = amount;
  transaction.timestamp = BigInt.fromString(event.timestamp.toString());
  transaction.operationHash = event.operation.hash;
  transaction.blockLevel = BigInt.fromString(event.block.level.toString());
  transaction.type = 'withdrawal';
  transaction.save();
}

export function handlePriceUpdate(event: any): void {
  // Extract data from the Tezos event
  let vaultId = event.source;
  let asset = event.parameters.asset;
  let price = BigInt.fromString(event.parameters.price);
  
  // Load or create vault
  let vault = Vault.load(vaultId);
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = vaultId;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = BigInt.fromString(event.timestamp.toString());
    vault.updatedAt = BigInt.fromString(event.timestamp.toString());
    vault.save();
  }
  
  // Create price update record
  let priceUpdateId = event.operation.hash + '-' + event.id;
  let priceUpdate = new PriceUpdate(priceUpdateId);
  priceUpdate.vault = vaultId;
  priceUpdate.asset = asset;
  priceUpdate.price = price;
  priceUpdate.timestamp = BigInt.fromString(event.timestamp.toString());
  priceUpdate.operationHash = event.operation.hash;
  priceUpdate.blockLevel = BigInt.fromString(event.block.level.toString());
  priceUpdate.save();
}