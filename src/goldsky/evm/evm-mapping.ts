vault.totalValue = BigInt.fromI32(DEFAULT_TOTAL_VALUE);
  
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
