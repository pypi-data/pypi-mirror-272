from web3 import Web3 
from eth_abi import abi
from pydantic import BaseModel
import json
from web3.middleware import geth_poa_middleware
import asyncio
from datetime import datetime, timedelta
from hexbytes import HexBytes
from eth_account.messages import encode_structured_data
import sys
from typing import Literal
import numpy as np


class EIP712PermitMessage(BaseModel):
    def getOneMonthDeadline():
        return int(datetime.now().timestamp() + 2592000)

    owner: str
    spender: str
    value: int
    nonce: int | None = None
    deadline: int | None = getOneMonthDeadline()


class EIP712PermitDomain(BaseModel):
    name: str
    chainId: int
    verifyingContract: str
    version: str | None = "1"


class EIP712Permit(BaseModel):
    types: dict = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "Permit": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "nonce", "type": "uint256"},
            {"name": "deadline", "type": "uint256"},
        ],
    }
    domain: EIP712PermitDomain
    primaryType: str = "Permit"
    message: EIP712PermitMessage


class SolidityParams(BaseModel):
    address: str = "address"
    uint256: str = "uint256"


class InputNativeTransfer(BaseModel):
    fromAddress: str
    fromAddressPK: str
    toAddress: str
    valueEther: str


class InputContract(BaseModel):
    contractAddress: str
    contractAbi: list
    functionName: str
    excuteArgs: list | None = []


class InputWriteContract(InputContract):
    fromAddress: str
    fromAddressPK: str | None = None


class InputGetEvent(BaseModel):
    contactAddress: str
    contractABI: list
    eventName: str
    fromBlock: int | str | None = "latest"
    toBlock: int | str | None = None
    argument_filters: dict | None = None
    topics: list | None = None


class LogFilter(BaseModel):
    fromBlock: int | str | None = "earliest"
    toBlock: int | str | None = "latest"
    address: str | list | None = None
    topics: list | None = None


ERC20Fn = Literal["transfer", "approve"]


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        return json.JSONEncoder.default(self, obj)


class Web3BlockChainUtils:
    def __init__(self, NODE_PROVIDER) -> None:
        self.NODE_PROVIDER = NODE_PROVIDER
        self.web3 = Web3(
            Web3.HTTPProvider(NODE_PROVIDER, request_kwargs={"timeout": 600})
        )
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)


class Web3Utils:
    def __init__(self, NODE_PROVIDER) -> None:
        self.NODE_PROVIDER = NODE_PROVIDER
        self.web3 = Web3(
            Web3.HTTPProvider(NODE_PROVIDER, request_kwargs={"timeout": 600})
        )
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    @staticmethod
    def getMax():
        return Web3.to_wei(2**64 - 1, "ether")

    @staticmethod
    def newAccount():
        web3 = Web3()
        account_new = web3.eth.account.create()
        account_json = {"address": account_new.address, "pk": account_new.key.hex()}
        return account_json

    @staticmethod
    def phaseAccount(privateKey):
        web3 = Web3()
        account = web3.eth.account.from_key(privateKey)
        account_json = {"address": account.address, "pk": account.key.hex()}
        return account_json

    @staticmethod
    def toChecksumAddress(adress: str):
        adress = Web3.to_checksum_address(adress)
        return adress

    @staticmethod
    def toChecksumAddresses(adresses: list):
        newList = []
        for address in adresses:
            address = Web3.to_checksum_address(address)
            newList.append(address)
        return newList

    def createContract(self, contractAddress, contractAbi):
        contractAddress = self.web3.to_checksum_address(contractAddress)
        contract = self.web3.eth.contract(address=contractAddress, abi=contractAbi)
        return contract

    def isContract(self, address):
        try:
            code = self.web3.eth.get_code(address)
        except:
            return False
        if code:
            return True
        else:
            return False

    def getBalance(self, address):
        return float(self.web3.from_wei(self.web3.eth.get_balance(address), "ether"))

    def getBalanceWei(self, address):
        return float(self.web3.eth.get_balance(address))

    async def estimateBaseGas(self):
        gasPrice = self.web3.eth.gas_price
        tx = {
            "chainId": self.web3.eth.chain_id,
            "gas": 21000,
            "gasPrice": gasPrice,
        }

        estimate_gas = self.web3.eth.estimate_gas(tx)
        return gasPrice * estimate_gas

    async def transferAllEth(self, toAddress: str, fromAddressPk: str):
        account = self.phaseAccount(fromAddressPk)
        toAddress = self.web3.to_checksum_address(toAddress)
        gasPrice = self.web3.eth.gas_price
        nonce = self.web3.eth.get_transaction_count(account["address"])
        balance = self.web3.eth.get_balance(account["address"])
        balanceTosend = balance - gasPrice * 21000
        if balance < gasPrice * 21000:
            return False
        tx = {
            "chainId": self.web3.eth.chain_id,
            "nonce": nonce,
            "to": toAddress,
            "value": balanceTosend,
            "gas": 21000,
            "gasPrice": gasPrice,
        }
        signed_tx = self.web3.eth.account.sign_transaction(tx, fromAddressPk)
        # print(signed_tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # print(tx_hash)
        for n in range(10):
            await asyncio.sleep(5)
            balanceTo = self.web3.eth.get_balance(toAddress)
            if balanceTo >= balanceTosend:
                break
        return self.web3.to_hex(tx_hash)

    async def transferAllTokens(
        self, toAddress: str, fromAddressPk: str, tokenAddress: list
    ):
        account = self.phaseAccount(fromAddressPk)
        tokenAddress = self.toChecksumAddresses(tokenAddress)
        result = []
        for token in tokenAddress:
            balanceWei = await self.ERC20BalanceOfWei(token, account["address"])
            if balanceWei <= 1:
                result.append({"token": token, "txhash": None})
                continue
            # print(balanceWei)
            txhash = await self.ERC20TransferWei(
                contractAddress=token,
                fromAddress=account["address"],
                fromAddressPK=account["pk"],
                toAddress=toAddress,
                valueWei=balanceWei - 1,
            )
            result.append({"token": token, "txhash": txhash})
            for n in range(10):
                await asyncio.sleep(5)
                balanceWei = await self.ERC20BalanceOfWei(token, account["address"])
                if balanceWei <= 1:
                    break
        return result

    async def nativeTokenTransaction(self, InputNativeTransfer: InputNativeTransfer):
        fromAddress = self.web3.to_checksum_address(InputNativeTransfer.fromAddress)
        toAddress = self.web3.to_checksum_address(InputNativeTransfer.toAddress)
        nonce = self.web3.eth.get_transaction_count(fromAddress)
        gasPrice = self.web3.eth.gas_price
        tx = {
            "chainId": self.web3.eth.chain_id,
            "nonce": nonce,
            "to": toAddress,
            "value": self.web3.to_wei(InputNativeTransfer.valueEther, "ether"),
            "gas": 21000,
            "gasPrice": gasPrice,
        }
        try:
            estimate_gas = self.web3.eth.estimate_gas(tx)
            tx.update({"gas": estimate_gas})

        except:
            # print("estimate_gas failed")
            pass
        signed_tx = self.web3.eth.account.sign_transaction(
            tx, InputNativeTransfer.fromAddressPK
        )
        # print(signed_tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # print(tx_hash)
        return self.web3.to_hex(tx_hash)

    async def excuteContractFunction(
        self, inputContract: InputContract, block_identifier="latest"
    ):
        ct = self.createContract(
            inputContract.contractAddress, inputContract.contractAbi
        )
        txFunction = eval(f"ct.functions.{inputContract.functionName}")
        result = txFunction(*inputContract.excuteArgs).call(
            block_identifier=block_identifier
        )
        return result

    async def estmaiteERC20Cost(
        self, contractAdress: str, excuteArgs: [], functionName: ERC20Fn
    ):
        inputContract = InputContract(
            contractAbi=ERC20ABI,
            contractAddress=contractAdress,
            excuteArgs=excuteArgs,
            functionName=functionName,
        )

        tx = await self.getContractWriteTxdata(inputContract)
        tx.update({"nonce": 0})
        estimate_gas = self.web3.eth.estimate_gas(tx)
        gasPrice = self.web3.eth.gas_price
        return gasPrice * estimate_gas

    async def getContractWriteTxdata(self, inputContract: InputContract):
        contractAddress = self.web3.to_checksum_address(inputContract.contractAddress)
        contract = self.web3.eth.contract(
            address=contractAddress, abi=inputContract.contractAbi
        )
        gasPrice = self.web3.eth.gas_price
        tx_info = {
            "chainId": self.web3.eth.chain_id,
            "gas": 200000000,
            "gasPrice": gasPrice,
        }
        tx_function = eval(f"contract.functions.{inputContract.functionName}")
        tx = tx_function(*inputContract.excuteArgs).build_transaction(tx_info)
        return tx

    async def excuteContractWriteFunction(self, inputWriteContract: InputWriteContract):
        fromAddress = self.web3.to_checksum_address(inputWriteContract.fromAddress)
        contractAddress = self.web3.to_checksum_address(
            inputWriteContract.contractAddress
        )
        nonce = self.web3.eth.get_transaction_count(fromAddress)
        contract = self.web3.eth.contract(
            address=contractAddress, abi=inputWriteContract.contractAbi
        )
        gasPrice = self.web3.eth.gas_price
        gasPrice = gasPrice * 2
        # print(f"successful get nonce{nonce}")
        tx_info = {
            "from": fromAddress,
            "nonce": nonce,
            "chainId": self.web3.eth.chain_id,
            "gas": 200000000,
            "gasPrice": gasPrice,
        }
        tx_function = eval(f"contract.functions.{inputWriteContract.functionName}")
        tx = tx_function(*inputWriteContract.excuteArgs).build_transaction(tx_info)
        estimate_gas = self.web3.eth.estimate_gas(tx)
        tx.update({"gas": estimate_gas})
        # print(tx)
        tx_signed = self.web3.eth.account.sign_transaction(
            tx, inputWriteContract.fromAddressPK
        )
        # print("successful sign transacions")
        tx_hash = self.web3.eth.send_raw_transaction(tx_signed.rawTransaction)
        # print("successful send transacions")
        # print(tx_hash)
        return self.web3.to_hex(tx_hash)

    async def ERC20Decimals(self, contractAddress):
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="decimals",
        )
        return await self.excuteContractFunction(inputContract)

    async def ERC20Symbol(self, contractAddress):
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="symbol",
        )
        return await self.excuteContractFunction(inputContract)

    async def ERC20totalSupply(self, contractAddress):
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="totalSupply",
        )
        return await self.excuteContractFunction(inputContract)

    async def ERC20totalEtherSupply(self, contractAddress):
        result = await asyncio.gather(
            self.ERC20totalSupply(contractAddress), self.ERC20Decimals(contractAddress)
        )

        totalEtherSupply = result[0] * 10 ** -result[1]
        return totalEtherSupply

    async def ERC20Allowance(self, contractAddress, owner, spender):
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="allowance",
            excuteArgs=[owner, spender],
        )
        return await self.excuteContractFunction(inputContract)

    async def ERC20BalanceOf(self, contractAddress, address):
        decimals = self.ERC20Decimals(contractAddress)
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="balanceOf",
            excuteArgs=[address],
        )
        balanceWei = self.excuteContractFunction(inputContract)
        result = await asyncio.gather(balanceWei, decimals)
        valueEther = Web3.from_wei(result[0], DECIMALSMAP[result[1]])
        return valueEther

    async def ERC20BalanceOfWei(self, contractAddress, address):
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="balanceOf",
            excuteArgs=[address],
        )
        balanceWei = await self.excuteContractFunction(inputContract)
        return balanceWei

    async def ERC20BalanceOftoBlock(self, contractAddress, address, toBlock):
        decimals = self.ERC20Decimals(contractAddress)
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="balanceOf",
            excuteArgs=[address],
        )
        balanceWei = self.excuteContractFunction(inputContract, toBlock)
        result = await asyncio.gather(balanceWei, decimals)
        valueEther = Web3.fromWei(result[0], DECIMALSMAP[result[1]])
        return valueEther

    async def ERC20Transfer(
        self, contractAddress, fromAddress, fromAddressPK, toAddress, valueEther
    ):
        decimals = await self.ERC20Decimals(contractAddress)
        valueWei = Web3.to_wei(valueEther, DECIMALSMAP[decimals])
        inputWriteContract = InputWriteContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="transfer",
            excuteArgs=[toAddress, valueWei],
            fromAddress=fromAddress,
            fromAddressPK=fromAddressPK,
        )
        return await self.excuteContractWriteFunction(inputWriteContract)

    async def ERC20TransferWei(
        self, contractAddress, fromAddress, fromAddressPK, toAddress, valueWei
    ):
        inputWriteContract = InputWriteContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="transfer",
            excuteArgs=[toAddress, valueWei],
            fromAddress=fromAddress,
            fromAddressPK=fromAddressPK,
        )
        return await self.excuteContractWriteFunction(inputWriteContract)

    async def ERC20TransferFromWei(
        self,
        contractAddress,
        fromAddress,
        toAddress,
        toAddressPK,
        valueWei,
        withdrawToAddress=None,
    ):
        # decimals = await self.ERC20Decimals(contractAddress)
        # valueWei = Web3.to_wei(valueEther, DECIMALSMAP[decimals])
        if not withdrawToAddress:
            withdrawToAddress = toAddress
        inputWriteContract = InputWriteContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="transferFrom",
            excuteArgs=[fromAddress, withdrawToAddress, valueWei],
            fromAddress=toAddress,
            fromAddressPK=toAddressPK,
        )
        return await self.excuteContractWriteFunction(inputWriteContract)

    async def ERC20Approve(
        self, contractAddress, fromAddress, fromAddressPK, toAddress, valueWei
    ):
        # decimals = await self.ERC20Decimals(contractAddress)
        # valueWei = Web3.to_wei(valueEther, DECIMALSMAP[decimals])
        inputWriteContract = InputWriteContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="approve",
            excuteArgs=[toAddress, valueWei],
            fromAddress=fromAddress,
            fromAddressPK=fromAddressPK,
        )
        return await self.excuteContractWriteFunction(inputWriteContract)

    async def ERC20Brun(self, contractAddress, fromAddress, fromAddressPK, valueEther):
        decimals = await self.ERC20Decimals(contractAddress)
        valueWei = Web3.to_wei(valueEther, DECIMALSMAP[decimals])
        inputWriteContract = InputWriteContract(
            contractAddress=contractAddress,
            contractAbi=ERC20ABI,
            functionName="burn",
            excuteArgs=[valueWei],
            fromAddress=fromAddress,
            fromAddressPK=fromAddressPK,
        )
        return await self.excuteContractWriteFunction(inputWriteContract)

    async def ERC20MetaData(self, contractAddress):
        task = [
            self.ERC20Symbol(contractAddress=contractAddress),
            self.ERC20totalSupply(contractAddress=contractAddress),
            self.ERC20Decimals(contractAddress=contractAddress),
        ]
        result = await asyncio.gather(*task)
        return result

    async def ERC20Nonces(self, contractAddress, address):
        abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"}
                ],
                "name": "nonces",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function",
            }
        ]
        inputContract = InputContract(
            contractAddress=contractAddress,
            contractAbi=abi,
            functionName="nonces",
            excuteArgs=[address],
        )
        return await self.excuteContractFunction(inputContract)

    async def ERC20SignPermit(self, eIP712Permit: EIP712Permit, pk):
        eIP712Permit.message.nonce = await self.ERC20Nonces(
            eIP712Permit.domain.verifyingContract, eIP712Permit.message.owner
        )

        encode_data = encode_structured_data(eIP712Permit.dict())
        signResult = self.web3.eth.account.sign_message(encode_data, pk)
        result = {
            "owner": eIP712Permit.message.owner,
            "spender": eIP712Permit.message.spender,
            "value": eIP712Permit.message.value,
            "deadline": eIP712Permit.message.deadline,
            "v": signResult.v,
            "r": self.web3.to_hex(signResult.r),
            "s": self.web3.to_hex(signResult.s),
        }
        # print(result)
        return result

    async def ERC20ExcutePermit(
        self, contractAddress: str, permit: dict, fromAddress, fromAddressPK
    ):
        abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "owner", "type": "address"},
                    {"internalType": "address", "name": "spender", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                    {"internalType": "uint8", "name": "v", "type": "uint8"},
                    {"internalType": "bytes32", "name": "r", "type": "bytes32"},
                    {"internalType": "bytes32", "name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ]
        inputContract = InputWriteContract(
            contractAddress=contractAddress,
            contractAbi=abi,
            functionName="permit",
            excuteArgs=[
                permit["owner"],
                permit["spender"],
                permit["value"],
                permit["deadline"],
                permit["v"],
                permit["r"],
                permit["s"],
            ],
            fromAddress=fromAddress,
            fromAddressPK=fromAddressPK,
        )
        result = await self.excuteContractWriteFunction(inputContract)
        return result

    async def checkTransactionStatus(self, hash):
        receipt = self.web3.eth.get_transaction_receipt(hash)
        if receipt["status"] == 1:
            return True
        else:
            return False

    async def estimateGas(self, _4byteSignatures: str, blockNumbers=5):
        blockDatas = await self.getLatestTransactions(blockNumbers)
        gaslist = []
        for blockData in blockDatas:
            for data in blockData:
                if self.web3.to_hex(data.input).startswith(_4byteSignatures):
                    gaslist.append(data.gas * data.gasPrice)
        if gaslist == []:
            gaslist = [0.00015 * 10**18]
        average = np.mean(gaslist)
        max = np.amax(gaslist)
        min = np.amin(gaslist)
        averageEther = self.web3.from_wei(average, "ether")
        result = {
            "average": average,
            "max": max,
            "economic": (average * 9 + min) / 10,
            "min": min,
            "averageEther": float(averageEther),
        }
        return result

    async def estimateApproveGas(self, blockNumbers=3):
        result = await self.estimateGas("0x095ea7b3", blockNumbers)
        return result

    async def getApproveGasFeed(
        self, fromAddress: str, fromAddressPK: str, toAddress: str, gasFeeWei
    ):
        inputNativeTransfer = InputNativeTransfer(
            fromAddress=fromAddress,
            fromAddressPK=fromAddressPK,
            toAddress=toAddress,
            valueEther=str(self.web3.from_wei(gasFeeWei, "ether")),
        )
        gasTransfer = await self.nativeTokenTransaction(inputNativeTransfer)
        return gasTransfer

    async def withdrawTokenFromtoAddress(
        self,
        contractAddress,
        fromAddress: str,
        fromAddressPK: str,
        toAddress: str,
        toAddressPK: str,
        gasFeeType="economic",
        blockNumbers=3,
        minAmount=0,
        withdrawToAddress=None,
    ):
        allowence = await self.ERC20Allowance(
            contractAddress=contractAddress, owner=toAddress, spender=fromAddress
        )
        balanceToken = await self.ERC20BalanceOfWei(
            contractAddress=contractAddress, address=toAddress
        )
        if balanceToken <= minAmount:
            return False
        # print(allowence, balanceToken)
        if allowence < balanceToken:
            balanceWei = self.getBalanceWei(toAddress)
            approveGas = await self.estimateApproveGas(blockNumbers)
            # print(approveGas)
            approveGas = approveGas[gasFeeType]
            # print(balanceWei, approveGas)
            if balanceWei < approveGas:
                print(f"{toAddressPK}-start-getApproveGasFeed")
                await self.getApproveGasFeed(
                    fromAddress=fromAddress,
                    fromAddressPK=fromAddressPK,
                    toAddress=toAddress,
                    gasFeeWei=approveGas,
                )
                for n in range(10):
                    await asyncio.sleep(5)
                    balanceWei = self.getBalanceWei(toAddress)
                    print(balanceWei, approveGas)
                    if balanceWei + 1 >= approveGas:
                        break
            print(f"{toAddressPK}-start-ERC20Approve")
            await self.ERC20Approve(
                contractAddress=contractAddress,
                fromAddress=toAddress,
                fromAddressPK=toAddressPK,
                toAddress=fromAddress,
                valueWei=self.getMax(),
            )
            for n in range(10):
                await asyncio.sleep(5)
                allowence = await self.ERC20Allowance(
                    contractAddress=contractAddress,
                    owner=toAddress,
                    spender=fromAddress,
                )
                print(allowence, balanceToken)
                if allowence >= balanceToken:
                    break
        print(f"{toAddressPK}-start-ERC20TransferFrom")

        txhash = await self.ERC20TransferFromWei(
            contractAddress=contractAddress,
            fromAddress=toAddress,
            toAddressPK=fromAddressPK,
            toAddress=fromAddress,
            valueWei=balanceToken,
            withdrawToAddress=withdrawToAddress,
        )
        return txhash

    async def getBlock(self, blockNumber="latest"):
        return self.web3.eth.get_block(blockNumber, full_transactions=True)

    async def getTimeStampByBlock(self, blockNumber="latest"):
        return self.web3.eth.get_block(blockNumber).timestamp

    async def getTimeUTC8ByBlock(self, blockNumber):
        utc8 = datetime.utcfromtimestamp(
            self.web3.eth.get_block(blockNumber).timestamp
        ) + timedelta(hours=8)

        return str(utc8)

    async def caculateAverageTime(self, fromBlock, toBlock):
        fromBlockData = self.getBlock(fromBlock)
        toBlockData = self.getBlock(toBlock)
        result = await asyncio.gather(fromBlockData, toBlockData)
        averageTime = (result[1]["timestamp"] - result[0]["timestamp"]) / (
            toBlock - fromBlock
        )
        return averageTime

    async def getBlockAverageTime(self):
        latestBlock = self.web3.eth.get_block("latest")
        latestNumber = latestBlock["number"]
        averageTime1000 = self.caculateAverageTime(latestNumber - 1000, latestNumber)
        averageTime10000 = self.caculateAverageTime(latestNumber - 10000, latestNumber)
        averageTime100000 = self.caculateAverageTime(
            latestNumber - 100000, latestNumber
        )
        result = await asyncio.gather(
            averageTime1000, averageTime10000, averageTime100000
        )
        average = sum(result) / len(result)
        return average

    async def getBlockByTimeStamp(self, timeStamp):
        latestBlock = self.getBlock()
        averageTime = self.getBlockAverageTime()
        result = await asyncio.gather(latestBlock, averageTime)
        estimateBlockNumber = int(
            result[0]["number"] - (result[0]["timestamp"] - timeStamp) / result[1]
        )
        estimateBlock = await self.getBlock(estimateBlockNumber)
        while True:
            if abs(estimateBlock["timestamp"] - timeStamp) > 10:
                blockDiff = abs((estimateBlock["timestamp"] - timeStamp) / result[1])

                if estimateBlock["timestamp"] > timeStamp:
                    estimateBlockNumberNew = int(estimateBlock["number"] - blockDiff)
                else:
                    estimateBlockNumberNew = int(estimateBlock["number"] + blockDiff)
                estimateBlock = await self.getBlock(estimateBlockNumberNew)
            else:
                break
        return estimateBlock

    async def getTransactionsByBlock(self, block_identifier, full_transactions=True):
        block = self.web3.eth.get_block(
            block_identifier=block_identifier, full_transactions=full_transactions
        )
        return block.transactions

    async def getTransactionsByBlockRange(self, fromBlock, toBlock):
        timeStart = datetime.now()
        latestBlockID = await self.getBlock()
        latestBlockID = latestBlockID["number"]
        if toBlock > latestBlockID:
            toBlock = latestBlockID
        tasks = []
        for bid in range(fromBlock, toBlock):
            tasks.append(self.getTransactionsByBlock(bid))
        result = await asyncio.gather(*tasks)
        timeEnd = datetime.now()
        print(f"起始区块{fromBlock}\n结束区块{toBlock}")
        print(f"任务区块数量实际扫区块数量{toBlock-fromBlock}")
        print(f"用时{timeEnd-timeStart}")
        return result

    async def getLatestTransactions(self, numbers=5):
        timeStart = datetime.now()
        latestBlockID = await self.getBlock()
        toBlock = latestBlockID["number"]
        tasks = []
        for bid in range(toBlock - numbers, toBlock):
            tasks.append(self.getTransactionsByBlock(bid))
        result = await asyncio.gather(*tasks)
        timeEnd = datetime.now()
        print(f"起始区块{toBlock-numbers}\n结束区块{toBlock}")
        print(f"任务区块数量实际扫区块数量{numbers}")
        print(f"用时{timeEnd-timeStart}")
        return result

    async def modifyBlockDatas(self, blockDatas):
        modifiedBlockDatas = []
        for bds in blockDatas:
            if bds == []:
                continue
            for bd in bds:
                bt = {}
                bt["blockNumber"] = bds[0].blockNumber
                bt["hash"] = bd.hash.hex()
                bt["from"] = bd["from"]
                bt["to"] = bd.to
                bt["input"] = bd.input
                modifiedBlockDatas.append(bt)
        modifiedBlockDatas.sort(key=lambda bd: bd["blockNumber"])
        return modifiedBlockDatas

    async def getLogs(self, logFilter: dict | LogFilter):
        if type(logFilter) == LogFilter:
            logFilter = logFilter.dict()
        logs = self.web3.eth.get_logs(logFilter)
        return await self.modifyLogs(logs)

    async def modifyLogs(self, logs):
        result = []
        for log in logs:
            log = log.__dict__
            dumpsLog = json.dumps(log, cls=MyEncoder)
            log = json.loads(dumpsLog)
            log["hash"] = self.web3.keccak(text=dumpsLog).hex()
            result.append(log)
        result.sort(key=lambda log: log["blockNumber"])
        return result

    async def getEevent(self, inputGetEvent: InputGetEvent):
        ct = self.createContract(
            inputGetEvent.contactAddress, inputGetEvent.contractABI
        )
        getEventFn = eval(
            f'ct.events.{inputGetEvent.eventName}.create_filter(fromBlock="{inputGetEvent.fromBlock}", toBlock="{inputGetEvent.toBlock}")'
        )
        # , argument_filters={inputGetEvent.argument_filters}
        # , topics={inputGetEvent.topics}
        result = Web3.toJSON(getEventFn)
        print(result)
        return result

    async def decodeInput(self, blockData, contractAbi):
        try:
            ct = self.createContract(blockData.get("to"), contractAbi)
            res = ct.decode_function_input(blockData["input"])
            res[1]["fn_name"] = res[0].fn_name
            blockData["input"] = res[1]
            return blockData
        except:
            # traceback.print_exc()
            blockData["decode"] = False
            return blockData

    async def decodeInputs(self, blockDatas: list, contract_abi):
        tasks = []
        for blockData in blockDatas:
            tasks.append(self.decodeInput(blockData, contract_abi))
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    def getEventsTop0ByAbi(abi):
        params = ""
        for p in abi["inputs"]:
            params = params + p["type"] + ","
        params = params.rstrip(",")
        temp = f'{abi["name"]}({params})'
        topic0 = Web3.keccak(text=temp).hex()
        return topic0

    @staticmethod
    def getEventsTop0ByAbis(abis):
        data = {}
        for abi in abis:
            try:
                data[f'{abi["name"]}'] = Web3Utils.getEventsTop0ByAbi(abi)
            except:
                continue
        with open("./eventsTopic0.json", "w+") as f:
            json.dump(data, f)
        return data


    @staticmethod
    def decodeParams(SolidityParams: list, hexdata: str | bytes):
        # eg. [uint256', 'address[]', 'uint256[]'] 
        if type(hexdata) == str:
            hexdata = bytes.fromhex(hexdata)
            # hexdata = bytes.fromhex(hexdata)
        res = abi.decode(SolidityParams, hexdata)
        return res

    @staticmethod
    def encodeParams(SolidityParams: list, data: list):
        res = "0x" + abi.encode(SolidityParams, data).hex()
        return res


class UniSwapUtils(Web3Utils):
    # async defd
    async def UV2_getReserves(self, address):
        inputContract = InputContract(
            contractAddress=address,
            contractAbi=UV2_PAIR_ABI,
            functionName="getReserves",
        )
        result = await self.excuteContractFunction(inputContract)
        return result

    async def UV2_price0CumulativeLast(self, address):
        inputContract = InputContract(
            contractAddress=address,
            contractAbi=UV2_PAIR_ABI,
            functionName="price0CumulativeLast",
        )
        result = await self.excuteContractFunction(inputContract)

        return result

    async def UV2_price1CumulativeLast(self, address):
        inputContract = InputContract(
            contractAddress=address,
            contractAbi=UV2_PAIR_ABI,
            functionName="price1CumulativeLast",
        )
        result = await self.excuteContractFunction(inputContract)

        return result

    async def UV2_totalSupply(self, address):
        inputContract = InputContract(
            contractAddress=address,
            contractAbi=UV2_PAIR_ABI,
            functionName="totalSupply",
        )
        result = await self.excuteContractFunction(inputContract)
        result = Web3.fromWei(result, "ether")
        return result

    async def UV2_PairMeta(self, address, token0, token1):
        tasks = [
            self.UV2_getReserves(address),
            self.UV2_totalSupply(address),
            self.UV2_price0CumulativeLast(address),
            self.UV2_price1CumulativeLast(address),
            self.ERC20totalSupply(token0),
            self.ERC20totalSupply(token1),
            self.ERC20Decimals(token0),
            self.ERC20Decimals(token1),
        ]
        result = await asyncio.gather(*tasks)
        # print(result)
        data = {
            "token0Total": result[4] * 10 ** -result[6],
            "reserve0": result[0][0] * 10 ** -result[6],
            "token1Total": result[5] * 10 ** -result[7],
            "reserve1": result[0][1] * 10 ** -result[7],
            "blockTimestampLast": result[0][2],
            "liquidity": result[1],
            "price0": result[2],
            "price1": result[3],
        }
        return data


ERC20ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "initialOwner", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {"inputs": [], "name": "CheckpointUnorderedInsertion", "type": "error"},
    {"inputs": [], "name": "ECDSAInvalidSignature", "type": "error"},
    {
        "inputs": [{"internalType": "uint256", "name": "length", "type": "uint256"}],
        "name": "ECDSAInvalidSignatureLength",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "s", "type": "bytes32"}],
        "name": "ECDSAInvalidSignatureS",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "increasedSupply", "type": "uint256"},
            {"internalType": "uint256", "name": "cap", "type": "uint256"},
        ],
        "name": "ERC20ExceededSafeSupply",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "allowance", "type": "uint256"},
            {"internalType": "uint256", "name": "needed", "type": "uint256"},
        ],
        "name": "ERC20InsufficientAllowance",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "uint256", "name": "balance", "type": "uint256"},
            {"internalType": "uint256", "name": "needed", "type": "uint256"},
        ],
        "name": "ERC20InsufficientBalance",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "approver", "type": "address"}],
        "name": "ERC20InvalidApprover",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "receiver", "type": "address"}],
        "name": "ERC20InvalidReceiver",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "sender", "type": "address"}],
        "name": "ERC20InvalidSender",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "spender", "type": "address"}],
        "name": "ERC20InvalidSpender",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "deadline", "type": "uint256"}],
        "name": "ERC2612ExpiredSignature",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "signer", "type": "address"},
            {"internalType": "address", "name": "owner", "type": "address"},
        ],
        "name": "ERC2612InvalidSigner",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "maxLoan", "type": "uint256"}],
        "name": "ERC3156ExceededMaxLoan",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "receiver", "type": "address"}],
        "name": "ERC3156InvalidReceiver",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"}],
        "name": "ERC3156UnsupportedToken",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
            {"internalType": "uint48", "name": "clock", "type": "uint48"},
        ],
        "name": "ERC5805FutureLookup",
        "type": "error",
    },
    {"inputs": [], "name": "ERC6372InconsistentClock", "type": "error"},
    {"inputs": [], "name": "EnforcedPause", "type": "error"},
    {"inputs": [], "name": "ExpectedPause", "type": "error"},
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "currentNonce", "type": "uint256"},
        ],
        "name": "InvalidAccountNonce",
        "type": "error",
    },
    {"inputs": [], "name": "InvalidShortString", "type": "error"},
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "OwnableInvalidOwner",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "OwnableUnauthorizedAccount",
        "type": "error",
    },
    {
        "inputs": [
            {"internalType": "uint8", "name": "bits", "type": "uint8"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "SafeCastOverflowedUintDowncast",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "string", "name": "str", "type": "string"}],
        "name": "StringTooLong",
        "type": "error",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "expiry", "type": "uint256"}],
        "name": "VotesExpiredSignature",
        "type": "error",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "value", "type": "uint256"}],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "burnFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "delegatee", "type": "address"}],
        "name": "delegate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "delegatee", "type": "address"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "uint256", "name": "expiry", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "delegateBySig",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "delegator",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "fromDelegate",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "toDelegate",
                "type": "address",
            },
        ],
        "name": "DelegateChanged",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "delegate",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "previousVotes",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newVotes",
                "type": "uint256",
            },
        ],
        "name": "DelegateVotesChanged",
        "type": "event",
    },
    {"anonymous": False, "inputs": [], "name": "EIP712DomainChanged", "type": "event"},
    {
        "inputs": [
            {
                "internalType": "contract IERC3156FlashBorrower",
                "name": "receiver",
                "type": "address",
            },
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "bytes", "name": "data", "type": "bytes"},
        ],
        "name": "flashLoan",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnershipTransferred",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "pause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address",
            }
        ],
        "name": "Paused",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "permit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "unpause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address",
            }
        ],
        "name": "Unpaused",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint32", "name": "pos", "type": "uint32"},
        ],
        "name": "checkpoints",
        "outputs": [
            {
                "components": [
                    {"internalType": "uint48", "name": "_key", "type": "uint48"},
                    {"internalType": "uint208", "name": "_value", "type": "uint208"},
                ],
                "internalType": "struct Checkpoints.Checkpoint208",
                "name": "",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "clock",
        "outputs": [{"internalType": "uint48", "name": "", "type": "uint48"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "CLOCK_MODE",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "delegates",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "DOMAIN_SEPARATOR",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "eip712Domain",
        "outputs": [
            {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "version", "type": "string"},
            {"internalType": "uint256", "name": "chainId", "type": "uint256"},
            {"internalType": "address", "name": "verifyingContract", "type": "address"},
            {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
            {"internalType": "uint256[]", "name": "extensions", "type": "uint256[]"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "flashFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "timepoint", "type": "uint256"}],
        "name": "getPastTotalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "timepoint", "type": "uint256"},
        ],
        "name": "getPastVotes",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "getVotes",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"}],
        "name": "maxFlashLoan",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "nonces",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "numCheckpoints",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "paused",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

DECIMALSMAP = {
    0: "noether",
    1: "wei",
    3: "kwei",
    6: "mwei",
    9: "gwei",
    12: "szabo",
    15: "milliether",
    18: "ether",
    21: "kether",
    24: "mether",
    27: "gether",
    30: "tether",
}
UV2_PAIR_ABI = json.loads(
    '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
)
