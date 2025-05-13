import { BigInt, Bytes, ethereum } from '@graphprotocol/graph-ts';
import {
  Deposit,
  Withdrawal,
  PriceUpdate
} from '../generated/VaultContract/VaultContract';
import { Vault, Transaction, PriceUpdate as PriceUpdateEntity } from '../generated/schema';

export function handleDeposit(event: Deposit): void {
  let vaultId = event.params.from.toHexString();
  let vault = Vault.load(vaultId);
  
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.params.from;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
  }
  
  vault.totalValue = vault.totalValue.plus(event.params.amount);
  vault.updatedAt = event.block.timestamp;
  vault.save();
  
  let transactionId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let transaction = new Transaction(transactionId);
  transaction.vault = vaultId;
  transaction.from = event.params.from;
  transaction.to = null;
  transaction.amount = event.params.amount;
  transaction.timestamp = event.block.timestamp;
  transaction.transactionHash = event.transaction.hash;
  transaction.blockNumber = event.block.number;
  transaction.type = 'deposit';
  transaction.save();
}

export function handleWithdrawal(event: Withdrawal): void {
  let vaultId = event.params.to.toHexString();
  let vault = Vault.load(vaultId);
  
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.params.to;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
  }
  
  // Withdrawal: ensure we don't go negative
  if (vault.totalValue.ge(event.params.amount)) {
    vault.totalValue = vault.totalValue.minus(event.params.amount);
  } else {
    // Handle insufficient funds case – here we zero out, but you may want to log or revert
    vault.totalValue = BigInt.fromI32(0);
  }
  vault.updatedAt = event.block.timestamp;
  vault.save();
  
  let transactionId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let transaction = new Transaction(transactionId);
  transaction.vault = vaultId;
  transaction.from = null;
  transaction.to = event.params.to;
  transaction.amount = event.params.amount;
  transaction.timestamp = event.block.timestamp;
  transaction.transactionHash = event.transaction.hash;
  transaction.blockNumber = event.block.number;
  transaction.type = 'withdrawal';
  transaction.save();
}

export function handlePriceUpdate(event: PriceUpdate): void {
  let vaultId = event.transaction.from.toHexString();
  let vault = Vault.load(vaultId);
  
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.transaction.from;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
    vault.updatedAt = event.block.timestamp;
    vault.save();
  }
  
  let priceUpdateId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let priceUpdate = new PriceUpdateEntity(priceUpdateId);
  priceUpdate.vault = vaultId;
  priceUpdate.asset = event.params.asset;
  priceUpdate.price = event.params.price;
  priceUpdate.timestamp = event.block.timestamp;
  priceUpdate.transactionHash = event.transaction.hash;
  priceUpdate.blockNumber = event.block.number;
  priceUpdate.save();
}