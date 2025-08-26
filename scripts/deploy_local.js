const { ethers } = require('ethers');
require('dotenv').config();

// Contract bytecode and ABI
const contractBytecode = '0x608060405234801561001057600080fd5b5061072b806100206000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c806308b8c6f81461005c578063940992a314610082578063962ea8ae146100a5578063a3112a64146100ad578063b1b76f99146100c0575b600080fd5b61006f61006a366004610423565b6100d5565b6040519081526020015b60405180910390f35b610095610090366004610423565b6100f6565b6040516100799493929190610482565b60015461006f565b6100956100bb366004610423565b6101b0565b6100d36100ce3660046104d0565b6102b1565b005b600181815481106100e557600080fd5b600091825260209091200154905081565b6000602081905290815260409020805460018201546002830180549293919261011e9061058b565b80601f016020809104026020016040519081016040528092919081815260200182805461014a9061058b565b80156101975780601f1061016c57610100808354040283529160200191610197565b820191906000526020600020905b81548152906001019060200180831161017a57829003601f168201915b505050600390930154919250506001600160a01b031684565b600080606060008060008087815260200190815260200160002060405180608001604052908160008201548152602001600182015481526020016002820180546101f99061058b565b80601f01602080910402602001604051908101604052809291908181526020018280546102259061058b565b80156102725780601f1061024757610100808354040283529160200191610272565b820191906000526020600020905b81548152906001019060200180831161025557829003601f168201915b5050509183525050600391909101546001600160a01b03166020918201528151908201516040830151606090930151919990985091965094509250505050565b816102f25760405162461bcd60e51b815260206004820152600c60248201526b092dcecc2d8d2c840d0c2e6d60a31b60448201526064015b60405180910390fd5b60008151116103365760405162461bcd60e51b815260206004820152601060248201526f125b9d985b1a5908189d5a5b1908125160821b60448201526064016102e9565b604080516080810182528381524260208083019182528284018581528282840183523360608501526000878152918290529390208251815590516001820155915190919060028201906103839082610614565b5060609190910151600390910180546001600160a01b0319166001600160a01b039092169190911790556001805480820182556000919091527fb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf601829055604051339083907f40e6001babf73511a8f89473ced520e880cd4abe5854bd494b7c32e1c36f50209061041790429086906106d4565b60405180910390a35050565b60006020828403121561043557600080fd5b5035919050565b6000815180845260005b8181101561046257602081850181015186830182015201610446565b506000602082860101526020601f19601f83011685010191505092915050565b8481528360208201526080604082015260006104a1608083018561043c565b905060018060a01b038316606083015295945050505050565b634e487b7160e01b600052604160045260246000fd5b600080604083850312156104e357600080fd5b82359150602083013567ffffffffffffffff8082111561050257600080fd5b818501915085601f83011261051657600080fd5b818501915085601f830112610528576105286104ba565b604051601f8201601f19908116603f01168101908382118183101715610550576105506104ba565b8160405282815288602084870101111561056957600080fd5b826020860160208301376000602084830101528095505050505050925092905050565b600181811c9082168061059f57607f821691505b6020821081036105bf57634e487b7160e01b600052602260045260246000fd5b50919050565b601f82111561060f57600081815260208120601f850160051c810160208610156105ec5750805b601f850160051c820191505b8181101561060b578281556001016105f8565b5050505050565b815167ffffffffffffffff81111561062e5761062e6104ba565b6106428161063c845461058b565b846105c5565b602080601f831160018114610677576000841561065f5750858301515b600019600386901b1c1916600185901b17855561060b565b600085815260208120601f198616915b828110156106a657888601518255948401946001909101908401610687565b50858210156106c45787850151600019600388901b60f8161c191681555b5050505050600190911b01905550565b8281526040602082015260006106ed604083018461043c565b94935050505056fea2646970667358221220c494693d8c9a68db12d5e05126c5e91efaa6d2f57328d0ca765a9ed4512ce86564736f6c63430008130033';

const contractABI = [
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "bytes32",
                "name": "hash",
                "type": "bytes32"
            },
            {
                "indexed": false,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "string",
                "name": "buildId",
                "type": "string"
            },
            {
                "indexed": true,
                "internalType": "address",
                "name": "attester",
                "type": "address"
            }
        ],
        "name": "AttestationStored",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "attestationHashes",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "name": "attestations",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "hash",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "buildId",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "attester",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_hash",
                "type": "bytes32"
            }
        ],
        "name": "getAttestation",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "hash",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "buildId",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "attester",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAttestationCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_hash",
                "type": "bytes32"
            },
            {
                "internalType": "string",
                "name": "_buildId",
                "type": "string"
            }
        ],
        "name": "storeAttestation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
];

async function deployContract() {
    try {
        console.log('🚀 Starting CraftX Attestation deployment...');

        // Configuration from environment variables
        const SEPOLIA_RPC_URL = process.env.ETHEREUM_RPC_URL || 'https://sepolia.infura.io/v3/0a3c044e0c7d45178b8d92aa6c17c77d';
        const PRIVATE_KEY = process.env.ETHEREUM_PRIVATE_KEY;

        if (!PRIVATE_KEY) {
            throw new Error('❌ ETHEREUM_PRIVATE_KEY environment variable is required');
        }

        // Setup provider and wallet
        const provider = new ethers.JsonRpcProvider(SEPOLIA_RPC_URL);
        const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

        console.log('📍 Deploying from account:', wallet.address);

        // Check network
        const network = await provider.getNetwork();
        console.log('🌐 Network:', network.name, 'Chain ID:', network.chainId.toString());

        if (network.chainId !== 11155111n) {
            throw new Error(`❌ Wrong network! Expected Sepolia (11155111), got ${network.chainId}`);
        }

        console.log('✅ Connected to Sepolia testnet');

        // Check balance
        const balance = await provider.getBalance(wallet.address);
        const balanceEth = ethers.formatEther(balance);
        console.log('💰 Account balance:', balanceEth, 'ETH');

        if (parseFloat(balanceEth) < 0.001) {
            throw new Error(`❌ Insufficient balance. Need at least 0.001 ETH for deployment. Current: ${balanceEth} ETH`);
        }

        // Get gas price and estimate cost
        const feeData = await provider.getFeeData();
        console.log('⛽ Current gas price:', ethers.formatUnits(feeData.gasPrice, 'gwei'), 'gwei');

        // Create contract factory
        const contractFactory = new ethers.ContractFactory(contractABI, contractBytecode, wallet);

        // Estimate gas
        const gasEstimate = await contractFactory.getDeployTransaction().then(tx =>
            provider.estimateGas(tx)
        );

        console.log('📊 Estimated gas:', gasEstimate.toString());

        // Calculate cost
        const estimatedCost = gasEstimate * feeData.gasPrice;
        console.log('💰 Estimated deployment cost:', ethers.formatEther(estimatedCost), 'ETH');

        // Deploy contract
        console.log('🚀 Deploying contract...');
        const contract = await contractFactory.deploy({
            gasLimit: gasEstimate + (gasEstimate * 20n / 100n), // Add 20% buffer
            gasPrice: feeData.gasPrice
        });

        console.log('⏳ Waiting for deployment transaction...');
        const receipt = await contract.deploymentTransaction().wait();

        console.log('✅ Contract deployed successfully!');
        console.log('📄 Transaction hash:', receipt.hash);
        console.log('📍 Contract address:', await contract.getAddress());
        console.log('⛽ Gas used:', receipt.gasUsed.toString());
        console.log('💸 Actual cost:', ethers.formatEther(receipt.gasUsed * receipt.gasPrice), 'ETH');
        console.log('📦 Block number:', receipt.blockNumber);

        // Verify deployment
        const deployedCode = await provider.getCode(await contract.getAddress());
        if (deployedCode === '0x') {
            throw new Error('❌ Contract deployment failed - no code at address');
        }

        console.log('✅ Contract verification successful');
        console.log('\n🎉 DEPLOYMENT COMPLETE!');
        console.log('🔗 Sepolia Etherscan:', `https://sepolia.etherscan.io/address/${await contract.getAddress()}`);
        console.log('🔗 Transaction:', `https://sepolia.etherscan.io/tx/${receipt.hash}`);

        console.log('\n📝 Save this for your GitHub CI configuration:');
        console.log(`ETHEREUM_CONTRACT_ADDRESS=${await contract.getAddress()}`);
        console.log(`ETHEREUM_DEPLOY_TX=${receipt.hash}`);

        // Test the contract
        console.log('\n🧪 Testing contract functionality...');
        const testHash = ethers.keccak256(ethers.toUtf8Bytes('test-attestation'));
        const testBuildId = 'test-build-001';

        console.log('📝 Storing test attestation...');
        const storeTx = await contract.storeAttestation(testHash, testBuildId);
        await storeTx.wait();
        console.log('✅ Test attestation stored!');

        // Retrieve the attestation
        const attestation = await contract.getAttestation(testHash);
        console.log('📖 Retrieved attestation:', {
            hash: attestation[0],
            timestamp: new Date(Number(attestation[1]) * 1000).toISOString(),
            buildId: attestation[2],
            attester: attestation[3]
        });

        console.log('✅ Contract is working correctly!');

        return {
            address: await contract.getAddress(),
            transactionHash: receipt.hash,
            blockNumber: receipt.blockNumber,
            gasUsed: receipt.gasUsed.toString(),
            cost: ethers.formatEther(receipt.gasUsed * receipt.gasPrice)
        };

    } catch (error) {
        console.error('❌ Deployment failed:', error.message);

        // Provide helpful troubleshooting
        if (error.message.includes('insufficient funds')) {
            console.log('\n💡 Troubleshooting: Get more Sepolia ETH from:');
            console.log('   • https://sepoliafaucet.com/');
            console.log('   • https://faucet.quicknode.com/ethereum/sepolia');
        }

        if (error.code === 'NETWORK_ERROR') {
            console.log('\n💡 Troubleshooting: Network connection issue');
            console.log('   • Check your internet connection');
            console.log('   • Verify Infura endpoint is working');
        }

        throw error;
    }
}

// Run deployment
if (require.main === module) {
    deployContract()
        .then((result) => {
            console.log('\n🎯 Deployment Summary:');
            console.log(JSON.stringify(result, null, 2));
            process.exit(0);
        })
        .catch((error) => {
            console.error('\n💥 Fatal error:', error);
            process.exit(1);
        });
}

module.exports = { deployContract };
