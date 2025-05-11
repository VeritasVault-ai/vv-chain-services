import { BigInt, Bytes, ethereum } from '@graphprotocol/graph-ts';
import {
  Deposit,
  Withdrawal,
  PriceUpdate,
  CrossChainOperation
} from '../generated/VaultContract/VaultContract';
import { Vault, Transaction, PriceUpdate as PriceUpdateEntity, CrossChainEvent } from '../generated/schema';

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
  if (vault.totalValue.ge(event.params.amount)) {
    vault.totalValue = vault.totalValue.minus(event.params.amount);
  } else {
    // Handle insufficient funds case - either log an error or set to zero
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

export function handleCrossChainOperation(event: CrossChainOperation): void {
  let vaultId = event.params.account.toHexString();
  let vault = Vault.load(vaultId);
  
  if (!vault) {
    vault = new Vault(vaultId);
    vault.owner = event.params.account;
    vault.totalValue = BigInt.fromI32(0);
    vault.createdAt = event.block.timestamp;
    vault.updatedAt = event.block.timestamp;
    vault.save();
  }
  
  let eventId = event.transaction.hash.toHexString() + '-' + event.logIndex.toString();
  let crossChainEvent = new CrossChainEvent(eventId);
  crossChainEvent.vault = vaultId;
  crossChainEvent.sourceChain = 'etherlink';
  crossChainEvent.destinationChain = event.params.targetChain.toString();
  crossChainEvent.amount = event.params.amount;
  crossChainEvent.status = 'initiated';
  crossChainEvent.timestamp = event.block.timestamp;
  crossChainEvent.transactionHash = event.transaction.hash;
  crossChainEvent.blockNumber = event.block.number;
  crossChainEvent.metadata = event.params.metadata;
  crossChainEvent.save();
}