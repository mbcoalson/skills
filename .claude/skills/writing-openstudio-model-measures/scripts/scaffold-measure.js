#!/usr/bin/env node

/**
 * OpenStudio ModelMeasure Scaffolding Script
 *
 * Creates a complete measure directory structure with boilerplate code.
 *
 * Usage:
 *   node scaffold-measure.js "Your Measure Name"
 *   node scaffold-measure.js "Add Window Overhangs" /path/to/measures/directory
 */

import { readFile, writeFile, mkdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Convert title case to snake_case for directory/class names
function toSnakeCase(str) {
  return str
    .replace(/([A-Z])/g, '_$1')
    .toLowerCase()
    .replace(/^_/, '')
    .replace(/\s+/g, '_')
    .replace(/_+/g, '_');
}

// Convert snake_case to TitleCase for class names
function toTitleCase(str) {
  return str
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('');
}

// Main scaffolding function
async function scaffoldMeasure(measureName, targetDir = '.') {
  console.log(`🏗️  Scaffolding OpenStudio ModelMeasure: "${measureName}"`);

  // Generate directory and class names
  const snakeName = toSnakeCase(measureName);
  const className = toTitleCase(snakeName);
  const measureDir = join(targetDir, snakeName);

  console.log(`   Directory: ${snakeName}/`);
  console.log(`   Class: ${className}`);

  // Check if directory already exists
  if (existsSync(measureDir)) {
    console.error(`❌ Error: Directory "${measureDir}" already exists.`);
    process.exit(1);
  }

  // Create directory structure
  console.log('\n📁 Creating directory structure...');
  await mkdir(measureDir, { recursive: true });
  await mkdir(join(measureDir, 'tests'), { recursive: true });
  await mkdir(join(measureDir, 'resources'), { recursive: true });

  console.log('   ✓ Created measure directory');
  console.log('   ✓ Created tests/ subdirectory');
  console.log('   ✓ Created resources/ subdirectory');

  // Load templates
  const templateDir = join(__dirname, '..', 'templates');
  const measureTemplate = await readFile(join(templateDir, 'model-measure-template.rb'), 'utf-8');
  const testTemplate = await readFile(join(templateDir, 'measure-test-template.rb'), 'utf-8');

  // Replace placeholders in measure.rb
  const measureContent = measureTemplate
    .replace(/YourMeasureName/g, className)
    .replace(/Your Measure Name/g, measureName);

  // Replace placeholders in test file
  const testContent = testTemplate
    .replace(/YourMeasureName/g, className);

  // Write measure.rb
  console.log('\n📝 Writing measure files...');
  await writeFile(join(measureDir, 'measure.rb'), measureContent, 'utf-8');
  console.log('   ✓ Created measure.rb');

  // Write test file
  await writeFile(join(measureDir, 'tests', `${snakeName}_test.rb`), testContent, 'utf-8');
  console.log(`   ✓ Created tests/${snakeName}_test.rb`);

  // Create README.md
  const readmeContent = `# ${measureName}

## Description

${measureName} is an OpenStudio ModelMeasure that modifies building energy models (.osm files).

## Modeler Description

[Add technical implementation details here]

## Measure Type

ModelMeasure

## Arguments

[Document measure arguments here]

## Outputs

[Document what the measure produces/modifies]

## Testing

Run the measure tests:

\`\`\`bash
cd ${snakeName}
ruby tests/${snakeName}_test.rb
\`\`\`

## Notes

[Add any additional notes, assumptions, or references here]
`;

  await writeFile(join(measureDir, 'README.md'), readmeContent, 'utf-8');
  console.log('   ✓ Created README.md');

  // Create LICENSE.md
  const licenseContent = `# License

Copyright (c) ${new Date().getFullYear()}

Licensed under the BSD 3-Clause License.
`;

  await writeFile(join(measureDir, 'LICENSE.md'), licenseContent, 'utf-8');
  console.log('   ✓ Created LICENSE.md');

  // Create .gitignore
  const gitignoreContent = `# OpenStudio measure files
measure.xml
*.osm~
*.idf~

# Test outputs
tests/output/

# Logs
*.log
`;

  await writeFile(join(measureDir, '.gitignore'), gitignoreContent, 'utf-8');
  console.log('   ✓ Created .gitignore');

  // Success message with next steps
  console.log('\n✅ Measure scaffolding complete!');
  console.log('\n📋 Next steps:');
  console.log(`   1. cd ${snakeName}`);
  console.log('   2. Edit measure.rb:');
  console.log('      - Update description() and modeler_description()');
  console.log('      - Add arguments in arguments() method');
  console.log('      - Implement measure logic in run() method');
  console.log(`   3. Edit tests/${snakeName}_test.rb to add test cases`);
  console.log('   4. Run tests: ruby tests/' + snakeName + '_test.rb');
  console.log('   5. Run in OpenStudio Application to generate measure.xml');
  console.log('\n📚 Documentation: https://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/');
}

// Parse command line arguments
const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('Usage: node scaffold-measure.js "Your Measure Name" [target_directory]');
  console.log('\nExample:');
  console.log('  node scaffold-measure.js "Add Window Overhangs"');
  console.log('  node scaffold-measure.js "Adjust Lighting Power" /path/to/measures');
  process.exit(1);
}

const measureName = args[0];
const targetDir = args[1] || '.';

// Run scaffolding
scaffoldMeasure(measureName, targetDir).catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
