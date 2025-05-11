import { BigInt, Bytes, Entity, store } from '@graphprotocol/graph-ts';

export class Vault extends Entity {
  constructor(id: string) {
    super();
    this.set("id", id);
  }

  save(): void {
    store.set("Vault", this.get("id").toString(), this);
  }

  static load(id: string): Vault | null {
    return store.get("Vault", id) as Vault | null;
  }

  get id(): string {
    return this.get("id").toString();
  }

  set owner(value: Bytes) {
    this.set("owner", value);
  }

  get owner(): Bytes {
    return this.get("owner") as Bytes;
  }

  set totalValue(value: BigInt) {
    this.set("totalValue", value);
  }

  get totalValue(): BigInt {
    return this.get("totalValue") as BigInt;
  }

  set createdAt(value: BigInt) {
    this.set("createdAt", value);
  }

  get createdAt(): BigInt {
    return this.get("createdAt") as BigInt;
  }

  set updatedAt(value: BigInt) {
    this.set("updatedAt", value);
  }

  get updatedAt(): BigInt {
    return this.get("updatedAt") as BigInt;
  }
}

export class Transaction extends Entity {
  constructor(id: string) {
    super();
    this.set("id", id);
  }

  save(): void {
    store.set("Transaction", this.get("id").toString(), this);
  }

  static load(id: string): Transaction | null {
    return store.get("Transaction", id) as Transaction | null;
  }

  get id(): string {
    return this.get("id").toString();
  }

  set vault(value: string) {
    this.set("vault", value);
  }

  get vault(): string {
    return this.get("vault").toString();
  }

  set from(value: Bytes | null) {
    if (value) {
      this.set("from", value);
    }
  }

  get from(): Bytes | null {
    return this.get("from") as Bytes | null;
  }

  set to(value: Bytes | null) {
    if (value) {
      this.set("to", value);
    }
  }

  get to(): Bytes | null {
    return this.get("to") as Bytes | null;
  }

  set amount(value: BigInt) {
    this.set("amount", value);
  }

  get amount(): BigInt {
    return this.get("amount") as BigInt;
  }

  set timestamp(value: BigInt) {
    this.set("timestamp", value);
  }

  get timestamp(): BigInt {
    return this.get("timestamp") as BigInt;
  }

  set transactionHash(value: Bytes) {
    this.set("transactionHash", value);
  }

  get transactionHash(): Bytes {
    return this.get("transactionHash") as Bytes;
  }

  set blockNumber(value: BigInt) {
    this.set("blockNumber", value);
  }

  get blockNumber(): BigInt {
    return this.get("blockNumber") as BigInt;
  }

  set type(value: string) {
    this.set("type", value);
  }

  get type(): string {
    return this.get("type").toString();
  }
}

export class PriceUpdate extends Entity {
  constructor(id: string) {
    super();
    this.set("id", id);
  }

  save(): void {
    store.set("PriceUpdate", this.get("id").toString(), this);
  }

  static load(id: string): PriceUpdate | null {
    return store.get("PriceUpdate", id) as PriceUpdate | null;
  }

  get id(): string {
    return this.get("id").toString();
  }

  set vault(value: string) {
    this.set("vault", value);
  }

  get vault(): string {
    return this.get("vault").toString();
  }

  set asset(value: string) {
    this.set("asset", value);
  }

  get asset(): string {
    return this.get("asset").toString();
  }

  set price(value: BigInt) {
    this.set("price", value);
  }

  get price(): BigInt {
    return this.get("price") as BigInt;
  }

  set timestamp(value: BigInt) {
    this.set("timestamp", value);
  }

  get timestamp(): BigInt {
    return this.get("timestamp") as BigInt;
  }

  set transactionHash(value: Bytes) {
    this.set("transactionHash", value);
  }

  get transactionHash(): Bytes {
    return this.get("transactionHash") as Bytes;
  }

  set blockNumber(value: BigInt) {
    this.set("blockNumber", value);
  }

  get blockNumber(): BigInt {
    return this.get("blockNumber") as BigInt;
  }
}