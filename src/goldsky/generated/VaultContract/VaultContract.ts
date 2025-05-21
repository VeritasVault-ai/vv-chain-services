import { BigInt, Address, ethereum } from '@graphprotocol/graph-ts';

// Event parameter interfaces
export class DepositParams {
  from: Address;
  amount: BigInt;
}

export class WithdrawalParams {
  to: Address;
  amount: BigInt;
}

export class PriceUpdateParams {
  asset: string;
  price: BigInt;
}

// Event interfaces
export class Deposit extends ethereum.Event {
  params: DepositParams;

  constructor(params: DepositParams) {
    super();
    this.params = params;
  }
}

export class Withdrawal extends ethereum.Event {
  params: WithdrawalParams;

  constructor(params: WithdrawalParams) {
    super();
    this.params = params;
  }
}

export class PriceUpdate extends ethereum.Event {
  params: PriceUpdateParams;

  constructor(params: PriceUpdateParams) {
    super();
    this.params = params;
  }
}

// Contract interface
export class VaultContract {
  address: Address;

  constructor(address: Address) {
    this.address = address;
  }
}