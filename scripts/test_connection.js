const { ethers } = require('ethers');
require('dotenv').config();

console.log('Testing environment...');
console.log('Node version:', process.version);
console.log('Ethers version:', require('ethers/package.json').version);
console.log('Private key loaded:', !!process.env.ETHEREUM_PRIVATE_KEY);
console.log('RPC URL loaded:', !!process.env.ETHEREUM_RPC_URL);

async function test() {
    try {
        const provider = new ethers.JsonRpcProvider(process.env.ETHEREUM_RPC_URL);
        const network = await provider.getNetwork();
        console.log('Network connection successful:', network.name, network.chainId.toString());

        if (process.env.ETHEREUM_PRIVATE_KEY) {
            const wallet = new ethers.Wallet(process.env.ETHEREUM_PRIVATE_KEY, provider);
            console.log('Wallet address:', wallet.address);

            const balance = await provider.getBalance(wallet.address);
            console.log('Balance:', ethers.formatEther(balance), 'ETH');
        }
    } catch (error) {
        console.error('Test failed:', error.message);
    }
}

test();
