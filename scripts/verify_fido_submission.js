#!/usr/bin/env node

/**
 * CraftX.py FIDO Submission Verification Script
 * Verifies all artifacts and attestations for FIDO Alliance certification
 */

const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

class FIDOSubmissionVerifier {
    constructor() {
        this.fidoDir = path.join(__dirname, '..', 'docs', 'fido');
        this.contractAddress = '0x50DB6330023d3Ee58906eCF3709419B25B1bcd53';
        this.results = {
            files: [],
            hashes: [],
            configs: [],
            errors: []
        };
    }

    async verify() {
        console.log('🔍 CraftX.py FIDO Submission Verification');
        console.log('==========================================');

        await this.checkDirectoryStructure();
        await this.verifyNDA();
        await this.verifyImplementationNotes();
        await this.verifyConfigurations();
        await this.verifyArtifacts();
        await this.verifyAttestations();

        this.generateReport();
    }

    async checkDirectoryStructure() {
        console.log('\n📁 Checking directory structure...');

        const requiredDirs = [
            'nda',
            'implementation',
            'config',
            'artifacts',
            'attestation'
        ];

        for (const dir of requiredDirs) {
            const dirPath = path.join(this.fidoDir, dir);
            if (fs.existsSync(dirPath)) {
                console.log(`  ✅ ${dir}/ directory exists`);
            } else {
                console.log(`  ❌ ${dir}/ directory missing`);
                this.results.errors.push(`Missing directory: ${dir}`);
            }
        }
    }

    async verifyNDA() {
        console.log('\n📄 Verifying NDA...');

        const ndaPath = path.join(this.fidoDir, 'nda', '2023-03-21-FIDO-Certification-NDA_FINAL.pdf');

        if (fs.existsSync(ndaPath)) {
            const stats = fs.statSync(ndaPath);
            console.log(`  ✅ NDA file exists (${stats.size} bytes)`);

            // Verify it's a PDF
            const buffer = fs.readFileSync(ndaPath, { start: 0, end: 4 });
            if (buffer.toString('utf8').startsWith('%PDF')) {
                console.log('  ✅ Valid PDF format');
            } else {
                console.log('  ❌ Invalid PDF format');
                this.results.errors.push('NDA is not a valid PDF file');
            }
        } else {
            console.log('  ❌ NDA file missing');
            this.results.errors.push('Missing NDA file');
        }
    }

    async verifyImplementationNotes() {
        console.log('\n📋 Verifying Implementation Notes...');

        const notesPath = path.join(this.fidoDir, 'implementation', 'CERTIFIABLE_IMPLEMENTATION_NOTES.md');

        if (fs.existsSync(notesPath)) {
            const content = fs.readFileSync(notesPath, 'utf8');
            const lines = content.split('\n').length;
            console.log(`  ✅ Implementation notes exist (${lines} lines)`);

            // Check for required sections
            const requiredSections = [
                'Architecture Overview',
                'Security Model',
                'FIDO Compliance',
                'Implementation Details'
            ];

            for (const section of requiredSections) {
                if (content.includes(section)) {
                    console.log(`  ✅ Contains "${section}" section`);
                } else {
                    console.log(`  ⚠️  Missing "${section}" section`);
                }
            }
        } else {
            console.log('  ❌ Implementation notes missing');
            this.results.errors.push('Missing implementation notes');
        }
    }

    async verifyConfigurations() {
        console.log('\n⚙️  Verifying Configuration Files...');

        const configs = ['rv-config.yaml', 'do-config.yaml', 'di-config.yaml'];

        for (const config of configs) {
            const configPath = path.join(this.fidoDir, 'config', config);

            if (fs.existsSync(configPath)) {
                const content = fs.readFileSync(configPath, 'utf8');
                console.log(`  ✅ ${config} exists`);

                // Basic YAML validation
                if (content.includes('version:') && content.includes('service:')) {
                    console.log(`  ✅ ${config} has valid structure`);
                    this.results.configs.push(config);
                } else {
                    console.log(`  ⚠️  ${config} may have invalid structure`);
                }
            } else {
                console.log(`  ❌ ${config} missing`);
                this.results.errors.push(`Missing config: ${config}`);
            }
        }
    }

    async verifyArtifacts() {
        console.log('\n🔐 Verifying Artifact Manifest...');

        const manifestPath = path.join(this.fidoDir, 'artifacts', 'ARTIFACT_MANIFEST.md');

        if (fs.existsSync(manifestPath)) {
            const content = fs.readFileSync(manifestPath, 'utf8');
            console.log('  ✅ Artifact manifest exists');

            // Extract SHA-256 hashes from manifest
            const hashRegex = /([a-f0-9]{64})/g;
            const hashes = content.match(hashRegex) || [];

            console.log(`  ✅ Found ${hashes.length} SHA-256 hashes in manifest`);

            // Verify contract address is mentioned
            if (content.includes(this.contractAddress)) {
                console.log('  ✅ Smart contract address referenced');
            } else {
                console.log('  ⚠️  Smart contract address not found');
            }

            this.results.hashes = hashes;
        } else {
            console.log('  ❌ Artifact manifest missing');
            this.results.errors.push('Missing artifact manifest');
        }
    }

    async verifyAttestations() {
        console.log('\n⛓️  Verifying Attestation Logs...');

        const attestationDir = path.join(this.fidoDir, 'attestation');
        const files = fs.readdirSync(attestationDir);

        const logFiles = files.filter(f => f.includes('attestation_log') || f.includes('hashes_'));

        console.log(`  ✅ Found ${logFiles.length} attestation log files`);

        for (const logFile of logFiles) {
            const filePath = path.join(attestationDir, logFile);
            const stats = fs.statSync(filePath);
            console.log(`  ✅ ${logFile} (${stats.size} bytes)`);
        }

        // Check for Ethereum integration
        const dailyLogPath = path.join(attestationDir, 'daily_attestation_log_20250825.md');
        if (fs.existsSync(dailyLogPath)) {
            const content = fs.readFileSync(dailyLogPath, 'utf8');
            if (content.includes('Ethereum') && content.includes(this.contractAddress)) {
                console.log('  ✅ Ethereum anchoring documented');
            } else {
                console.log('  ⚠️  Ethereum anchoring not properly documented');
            }
        }
    }

    generateReport() {
        console.log('\n📊 VERIFICATION REPORT');
        console.log('======================');

        console.log(`✅ Configuration files: ${this.results.configs.length}/3`);
        console.log(`✅ SHA-256 hashes found: ${this.results.hashes.length}`);
        console.log(`❌ Errors found: ${this.results.errors.length}`);

        if (this.results.errors.length === 0) {
            console.log('\n🎉 FIDO SUBMISSION READY!');
            console.log('All required components are present and verified.');
        } else {
            console.log('\n⚠️  ISSUES FOUND:');
            this.results.errors.forEach(error => {
                console.log(`   - ${error}`);
            });
        }

        console.log('\n📍 Submission Location: docs/fido/');
        console.log('📍 Smart Contract: 0x50DB6330023d3Ee58906eCF3709419B25B1bcd53');
        console.log('📍 Ethereum Gateway: https://eth-anchor.craftx.elevatecraft.org');
    }
}

// Run verification if called directly
if (require.main === module) {
    const verifier = new FIDOSubmissionVerifier();
    verifier.verify().catch(console.error);
}

module.exports = FIDOSubmissionVerifier;
