#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');

// Get the path to the goldsky executable
const goldsky = path.join(process.env.APPDATA, 'npm', 'node_modules', '@goldskycom', 'cli', 'bin', 'goldsky.js');

console.log('Deploying EtherLink subgraph...');

try {
  // Change to the etherlink directory
  process.chdir(path.join(__dirname, 'etherlink'));
  
  // Run the deployment command
  const command = `node "${goldsky}" subgraph deploy veritasvault/etherlink-mainnet --network etherlink-mainnet --from-config subgraph.yaml`;
  console.log(`Executing: ${command}`);
  const output = execSync(command, { encoding: 'utf8' });
  // Sanitize any sensitive information before logging
  const sanitizedOutput = output.replace(/token=[\w-]+/g, 'token=***');
  console.log(sanitizedOutput);
  
  console.log('EtherLink subgraph deployed successfully!');
  
  // Set up webhook
  const webhookCommand = `node "${goldsky}" subgraph webhook create veritasvault/etherlink-mainnet --endpoint https://veritasvault-eventgrid.azure-api.net/api/events --secret $WEBHOOK_API_KEY`;
  console.log(`Setting up webhook: ${webhookCommand}`);
  
  const webhookOutput = execSync(webhookCommand, { encoding: 'utf8' });
  console.log(webhookOutput);
  
  console.log('Webhook configured successfully!');
} catch (error) {
  console.error('Error deploying EtherLink subgraph:', error.message);
  process.exit(1);
}