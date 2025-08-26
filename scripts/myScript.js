// @custom:dev-run-script
// CraftX Attestation Contract Deployment Script for Remix IDE

(async () => {
    try {
        console.log('🚀 Starting CraftX Attestation deployment...');
        
        // Verify we're on Sepolia testnet
        const networkId = await web3.eth.net.getId();
        console.log('Network ID:', networkId);
        
        if (networkId !== 11155111) {
            throw new Error('❌ Please switch to Sepolia testnet (Network ID: 11155111). Currently on network: ' + networkId);
        }
        
        console.log('✅ Connected to Sepolia testnet');

        // Get the current selected account from MetaMask/Remix
        const accounts = await web3.eth.getAccounts();
        if (accounts.length === 0) {
            throw new Error('❌ No accounts found. Please connect your MetaMask wallet.');
        }
        
        const deployerAddress = accounts[0];
        console.log('📍 Deploying from account:', deployerAddress);
        
        // Check balance
        const balance = await web3.eth.getBalance(deployerAddress);
        const balanceEth = web3.utils.fromWei(balance, 'ether');
        console.log('💰 Account balance:', balanceEth, 'ETH');
        
        if (parseFloat(balanceEth) < 0.001) {
            throw new Error(`❌ Insufficient balance. Need at least 0.001 ETH for deployment. Current: ${balanceEth} ETH`);
        }

        // Contract bytecode (from compiled CraftXAttestation contract)
        const contractBytecode = '0x608060405234801561001057600080fd5b5061072b806100206000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c806308b8c6f81461005c578063940992a314610082578063962ea8ae146100a5578063a3112a64146100ad578063b1b76f99146100c0575b600080fd5b61006f61006a366004610423565b6100d5565b6040519081526020015b60405180910390f35b610095610090366004610423565b6100f6565b6040516100799493929190610482565b60015461006f565b6100956100bb366004610423565b6101b0565b6100d36100ce3660046104d0565b6102b1565b005b600181815481106100e557600080fd5b600091825260209091200154905081565b6000602081905290815260409020805460018201546002830180549293919261011e9061058b565b80601f016020809104026020016040519081016040528092919081815260200182805461014a9061058b565b80156101975780601f1061016c57610100808354040283529160200191610197565b820191906000526020600020905b81548152906001019060200180831161017a57829003601f168201915b505050600390930154919250506001600160a01b031684565b600080606060008060008087815260200190815260200160002060405180608001604052908160008201548152602001600182015481526020016002820180546101f99061058b565b80601f01602080910402602001604051908101604052809291908181526020018280546102259061058b565b80156102725780601f1061024757610100808354040283529160200191610272565b820191906000526020600020905b81548152906001019060200180831161025557829003601f168201915b5050509183525050600391909101546001600160a01b03166020918201528151908201516040830151606090930151919990985091965094509250505050565b816102f25760405162461bcd60e51b815260206004820152600c60248201526b092dcecc2d8d2c840d0c2e6d60a31b60448201526064015b60405180910390fd5b60008151116103365760405162461bcd60e51b815260206004820152601060248201526f125b9d985b1a5908189d5a5b1908125160821b60448201526064016102e9565b604080516080810182528381524260208083019182528284018581528282840183523360608501526000878152918290529390208251815590516001820155915190919060028201906103839082610614565b5060609190910151600390910180546001600160a01b0319166001600160a01b039092169190911790556001805480820182556000919091527fb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf601829055604051339083907f40e6001babf73511a8f89473ced520e880cd4abe5854bd494b7c32e1c36f50209061041790429086906106d4565b60405180910390a35050565b60006020828403121561043557600080fd5b5035919050565b6000815180845260005b8181101561046257602081850181015186830182015201610446565b506000602082860101526020601f19601f83011685010191505092915050565b8481528360208201526080604082015260006104a1608083018561043c565b905060018060a01b038316606083015295945050505050565b634e487b7160e01b600052604160045260246000fd5b600080604083850312156104e357600080fd5b82359150602083013567ffffffffffffffff8082111561050257600080fd5b818501915085601f83011261051657600080fd5b818501915085601f830112610528576105286104ba565b604051601f8201601f19908116603f01168101908382118183101715610550576105506104ba565b8160405282815288602084870101111561056957600080fd5b826020860160208301376000602084830101528095505050505050925092905050565b600181811c9082168061059f57607f821691505b6020821081036105bf57634e487b7160e01b600052602260045260246000fd5b50919050565b601f82111561060f57600081815260208120601f850160051c810160208610156105ec5750805b601f850160051c820191505b8181101561060b578281556001016105f8565b5050505050565b815167ffffffffffffffff81111561062e5761062e6104ba565b6106428161063c845461058b565b846105c5565b602080601f831160018114610677576000841561065f5750858301515b600019600386901b1c1916600185901b17855561060b565b600085815260208120601f198616915b828110156106a657888601518255948401946001909101908401610687565b50858210156106c45787850151600019600388901b60f8161c191681555b5050505050600190911b01905550565b8281526040602082015260006106ed604083018461043c565b94935050505056fea2646970667358221220c494693d8c9a68db12d5e05126c5e91efaa6d2f57328d0ca765a9ed4512ce86564736f6c63430008130033';

        // Get optimal gas price using your Infura endpoint
        try {
            const gasResponse = await fetch('https://gas.api.infura.io/v3/0a3c044e0c7d45178b8d92aa6c17c77d');
            const gasData = await gasResponse.json();
            console.log('📊 Current gas prices (gwei):', {
                slow: gasData.slow,
                standard: gasData.standard,
                fast: gasData.fast
            });
        } catch (gasError) {
            console.log('⚠️ Could not fetch gas prices, using network default');
        }

        // Estimate gas for deployment
        const gasEstimate = await web3.eth.estimateGas({
            data: contractBytecode,
            from: deployerAddress
        });
        console.log('⛽ Estimated gas:', gasEstimate);

        // Get current gas price from network
        const gasPrice = await web3.eth.getGasPrice();
        const gasPriceGwei = web3.utils.fromWei(gasPrice, 'gwei');
        console.log('💸 Current gas price:', gasPriceGwei, 'gwei');

        // Calculate deployment cost
        const deploymentCost = web3.utils.fromWei((BigInt(gasEstimate) * BigInt(gasPrice)).toString(), 'ether');
        console.log('💰 Estimated deployment cost:', deploymentCost, 'ETH');

        // Deploy the contract
        const deployTx = {
            data: contractBytecode,
            from: deployerAddress,
            gas: Math.round(gasEstimate * 1.2), // Add 20% buffer
            gasPrice: gasPrice
        };

        console.log('🚀 Sending deployment transaction...');
        const receipt = await web3.eth.sendTransaction(deployTx);

        console.log('✅ Contract deployed successfully!');
        console.log('📄 Transaction hash:', receipt.transactionHash);
        console.log('📍 Contract address:', receipt.contractAddress);
        console.log('⛽ Gas used:', receipt.gasUsed);
        console.log('💸 Actual cost:', web3.utils.fromWei((BigInt(receipt.gasUsed) * BigInt(gasPrice)).toString(), 'ether'), 'ETH');

        // Verify contract is deployed
        const code = await web3.eth.getCode(receipt.contractAddress);
        if (code === '0x') {
            throw new Error('Contract deployment failed - no code at address');
        }

        console.log('✅ Contract verification successful');
        console.log('\n🎉 DEPLOYMENT COMPLETE!');
        console.log('🔗 Sepolia Etherscan:', `https://sepolia.etherscan.io/address/${receipt.contractAddress}`);
        console.log('📋 Contract Address:', receipt.contractAddress);
        console.log('\n📝 Save this address for your GitHub CI configuration:');
        console.log(`ETHEREUM_CONTRACT_ADDRESS=${receipt.contractAddress}`);

        return receipt.contractAddress;

    } catch (error) {
        console.error('❌ Deployment failed:', error.message);
        console.error('📋 Full error details:', error);
        
        // Provide helpful troubleshooting
        if (error.message.includes('insufficient funds')) {
            console.log('\n💡 Troubleshooting: Get more Sepolia ETH from:');
            console.log('   • https://sepoliafaucet.com/');
            console.log('   • https://faucet.quicknode.com/ethereum/sepolia');
        }
        
        if (error.message.includes('network')) {
            console.log('\n💡 Troubleshooting: Ensure you are:');
            console.log('   • Connected to Sepolia testnet in MetaMask');
            console.log('   • Using the correct RPC endpoint');
        }
        
        throw error;
    }
})();
