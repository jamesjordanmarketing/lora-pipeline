#!/usr/bin/env node

/**
 * Integration Spec Merger (v2)
 * 
 * Purpose: Merge structured specification with integration knowledge to produce
 *          an integrated extension specification.
 * 
 * Interactive script with default paths based on product abbreviation.
 * 
 * Usage:
 *   From pmc/product/_tools/, run:
 *     node 04e-merge-integration-spec_v2.js "Project Name" product-abbreviation
 * 
 * Examples:
 *     node 04e-merge-integration-spec_v2.js "LoRA Pipeline" pipeline
 *     node 04e-merge-integration-spec_v2.js "Bright Module Orchestrator" bmo
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Create readline interface for user interaction
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Promisify readline question
function question(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

// Convert path to display format (full absolute path)
function toDisplayPath(absolutePath) {
  const normalized = absolutePath.replace(/\\/g, '/');
  return normalized;
}

// Validate that a file exists
function validatePath(filePath, shouldExist = true) {
  const exists = fs.existsSync(filePath);
  
  if (shouldExist && !exists) {
    return { valid: false, message: `File does not exist: ${toDisplayPath(filePath)}` };
  }
  
  if (!shouldExist && exists) {
    return { 
      valid: true, 
      warning: `Warning: File already exists and will be overwritten: ${toDisplayPath(filePath)}` 
    };
  }
  
  return { valid: true };
}

// Resolve various path formats to absolute paths
function resolvePath(inputPath) {
  // Handle absolute Windows paths
  if (inputPath.match(/^[A-Za-z]:\\/)) {
    return path.normalize(inputPath);
  }
  
  // Handle relative paths
  if (inputPath.startsWith('../') || inputPath.startsWith('./')) {
    return path.resolve(__dirname, inputPath);
  }
  
  // Handle paths relative to project root
  if (inputPath.startsWith('pmc/')) {
    return path.resolve(__dirname, '../..', inputPath);
  }
  
  // Default: treat as relative to current directory
  return path.resolve(process.cwd(), inputPath);
}

// Get a valid file path from user
async function getValidPath(promptText, defaultPath, shouldExist = true) {
  while (true) {
    const resolvedDefault = resolvePath(defaultPath);
    const validation = validatePath(resolvedDefault, shouldExist);
    
    console.log(`\n${promptText}`);
    console.log(`Default: ${toDisplayPath(resolvedDefault)}`);
    
    if (validation.warning) {
      console.log(`⚠️  ${validation.warning}`);
    }
    
    const input = await question('> ');
    
    // Use default if empty input
    if (!input.trim()) {
      if (validation.valid) {
        return resolvedDefault;
      } else {
        console.log(`❌ ${validation.message}`);
        continue;
      }
    }
    
    // Validate user input
    const resolvedInput = resolvePath(input.trim());
    const inputValidation = validatePath(resolvedInput, shouldExist);
    
    if (inputValidation.valid) {
      if (inputValidation.warning) {
        console.log(`⚠️  ${inputValidation.warning}`);
        const confirm = await question('Continue? (y/n): ');
        if (confirm.toLowerCase() !== 'y') {
          continue;
        }
      }
      return resolvedInput;
    } else {
      console.log(`❌ ${inputValidation.message}`);
    }
  }
}

// Read file content
function readFile(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error.message);
    process.exit(1);
  }
}

// Write file content
function writeFile(filePath, content) {
  try {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`📁 Created directory: ${toDisplayPath(dir)}`);
    }
    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`✅ Written: ${toDisplayPath(filePath)}`);
  } catch (error) {
    console.error(`Error writing file ${filePath}:`, error.message);
    process.exit(1);
  }
}

// ============================================================================
// TRANSFORMATION LOGIC (from v1)
// ============================================================================

const CONFIG = {
  substitutions: {
    'Prisma': 'Supabase Client (direct queries)',
    'NextAuth.js': 'Supabase Auth',
    'NextAuth': 'Supabase Auth',
    'AWS S3': 'Supabase Storage',
    'S3': 'Supabase Storage',
    'BullMQ': 'Supabase Edge Functions + Cron',
    'Redis': 'Supabase Edge Functions + Cron',
    'SWR': 'React Query',
    'Server-Sent Events': 'React Query polling',
    'SSE': 'React Query polling',
  },
};

function extractSections(specContent) {
  const sections = [];
  const sectionRegex = /## SECTION (\d+):\s*(.+?)(?=\n## SECTION \d+:|$)/gs;
  
  let match;
  while ((match = sectionRegex.exec(specContent)) !== null) {
    const sectionNumber = parseInt(match[1]);
    const fullContent = match[0];
    const titleMatch = fullContent.match(/## SECTION \d+:\s*(.+)/);
    const title = titleMatch ? titleMatch[1].trim() : 'Unknown';
    
    sections.push({
      number: sectionNumber,
      title: title,
      content: fullContent,
      originalContent: fullContent,
    });
  }
  
  return sections;
}

function extractFeatures(sectionContent) {
  const features = [];
  const featureRegex = /#### (FR-\d+\.\d+(?:\.\d+)?):(.+?)(?=\n#### FR-|\n### |$)/gs;
  
  let match;
  while ((match = featureRegex.exec(sectionContent)) !== null) {
    features.push({
      id: match[1],
      content: match[0],
    });
  }
  
  return features;
}

function transformSection(section, inventory, strategy, guide, projectName) {
  // For Section 1, provide comprehensive foundation notes
  if (section.number === 1) {
    return `## SECTION 1: Foundation & Authentication - INTEGRATED

**Project**: ${projectName}
**Extension Status**: ✅ Most infrastructure ALREADY EXISTS - only adding module-specific tables

**What Already Exists** (from existing codebase):
- ✅ Next.js 14 App Router with TypeScript
- ✅ Supabase Auth with cookie-based sessions
- ✅ Supabase PostgreSQL database with direct client
- ✅ Supabase Storage with on-demand signed URLs
- ✅ shadcn/ui components (47+ components available)
- ✅ React Query for state management
- ✅ Dashboard layout and protected routes

**What We're Adding** (${projectName} specific):
- New database tables for module functionality
- New storage buckets (if needed)
- New type definitions

**Infrastructure Patterns to USE**:
- Authentication: Use \`requireAuth()\` from \`@/lib/supabase-server\`
- Database: Use \`createServerSupabaseClient()\` for queries
- Storage: Use \`createServerSupabaseAdminClient()\` for signed URLs
- Components: Import from \`@/components/ui/\`
- API Routes: Follow existing response format \`{ success, data }\` or \`{ error, details }\`

---

${section.content}

---

`;
  }
  
  // For other sections, add integration markers
  const originalInfra = identifyOriginalInfrastructure(section.content);
  const actualInfra = originalInfra.map(item => CONFIG.substitutions[item] || item);
  
  let transformed = `## SECTION ${section.number}: ${section.title} - INTEGRATED

**Project**: ${projectName}
**Extension Status**: ✅ Transformed to use existing infrastructure  
**Original Infrastructure**: ${originalInfra.join(', ') || 'None specified'}  
**Actual Infrastructure**: ${actualInfra.join(', ') || 'Using existing patterns'}

---

${section.content}

---

`;
  
  return transformed;
}

function identifyOriginalInfrastructure(content) {
  const mentioned = new Set();
  
  for (const [key, value] of Object.entries(CONFIG.substitutions)) {
    const regex = new RegExp(`\\b${key}\\b`, 'gi');
    if (regex.test(content)) {
      mentioned.add(key);
    }
  }
  
  return Array.from(mentioned);
}

function generateHeader(projectName) {
  const date = new Date().toISOString().split('T')[0];
  
  return `# ${projectName} - Integrated Extension Specification

**Version:** 1.0  
**Date:** ${date}  
**Generated by:** 04e-merge-integration-spec_v2.js

---

## INTEGRATION SUMMARY

This specification describes how to implement the ${projectName} as an EXTENSION to the existing BrightHub application.

**Approach**: EXTENSION (not separate application)

**Infrastructure Decisions**:
- ✅ Use existing Supabase Auth (not NextAuth)
- ✅ Use existing Supabase PostgreSQL (not Prisma)
- ✅ Use existing Supabase Storage (not S3)
- ✅ Use existing shadcn/ui components
- ✅ Use existing React Query (not SWR)
- ✅ Use Edge Functions + Cron (not BullMQ + Redis)

**What We're Adding**:
- New database tables for ${projectName}
- New storage buckets (if needed)
- New API routes
- New pages
- New components
- New hooks
- Edge Functions (if needed)

**What We're NOT Creating**:
- ❌ New authentication system
- ❌ New database client
- ❌ New storage client
- ❌ Job queue infrastructure
- ❌ Component library

---

`;
}

function generateFooter() {
  return `
---

## APPENDIX: Integration Reference

### Infrastructure Inventory Cross-Reference

For detailed patterns and exact code examples, refer to:
- **Section 1 (Auth)**: Infrastructure Inventory - Authentication patterns with requireAuth()
- **Section 2 (Database)**: Infrastructure Inventory - Supabase Client query patterns
- **Section 3 (Storage)**: Infrastructure Inventory - On-demand signed URL generation
- **Section 4 (API)**: Infrastructure Inventory - API route templates and response formats
- **Section 5 (Components)**: Infrastructure Inventory - shadcn/ui component usage
- **Section 6 (State)**: Infrastructure Inventory - React Query hook patterns

---

**Document Status**: ✅ READY FOR SEGMENTATION  
**Next Step**: Run segmentation script (04f-segment-integrated-spec_v2.js)
`;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  try {
    // Check for required command-line arguments
    const args = process.argv.slice(2);
    if (args.length !== 2) {
      console.error('Usage: node 04e-merge-integration-spec_v2.js "Project Name" product-abbreviation');
      console.error('Example:');
      console.error('  node 04e-merge-integration-spec_v2.js "LoRA Pipeline" pipeline');
      process.exit(1);
    }
    
    const [projectName, productAbbreviation] = args;
    
    console.log('\n╔════════════════════════════════════════════════════════════╗');
    console.log('║         Integration Spec Merger (Interactive v2)          ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');
    console.log(`Project: ${projectName} (${productAbbreviation})\n`);
    
    // Step 1: Get structured spec path
    console.log('Step 1: Locate Structured Specification');
    console.log('─────────────────────────────────────────');
    
    const defaultSpecPath = path.resolve(
      __dirname, 
      '..', 
      '_mapping', 
      productAbbreviation, 
      `04c-${productAbbreviation}-structured-from-wireframe_v1.md`
    );
    
    const specPath = await getValidPath(
      'Enter path to structured specification:',
      defaultSpecPath,
      true
    );
    
    console.log(`✓ Using structured spec: ${toDisplayPath(specPath)}`);
    
    // Step 2: Get infrastructure inventory path
    console.log('\n\nStep 2: Locate Infrastructure Inventory');
    console.log('────────────────────────────────────────');
    
    const defaultInventoryPath = path.resolve(
      __dirname,
      '..',
      '_mapping',
      productAbbreviation,
      '_run-prompts',
      `04d-${productAbbreviation}-infrastructure-inventory_v1.md`
    );
    
    const inventoryPath = await getValidPath(
      'Enter path to infrastructure inventory:',
      defaultInventoryPath,
      true
    );
    
    console.log(`✓ Using inventory: ${toDisplayPath(inventoryPath)}`);
    
    // Step 3: Get extension strategy path
    console.log('\n\nStep 3: Locate Extension Strategy');
    console.log('──────────────────────────────────');
    
    const defaultStrategyPath = path.resolve(
      __dirname,
      '..',
      '_mapping',
      productAbbreviation,
      '_run-prompts',
      `04d-${productAbbreviation}-extension-strategy_v1.md`
    );
    
    const strategyPath = await getValidPath(
      'Enter path to extension strategy:',
      defaultStrategyPath,
      true
    );
    
    console.log(`✓ Using strategy: ${toDisplayPath(strategyPath)}`);
    
    // Step 4: Get implementation guide path
    console.log('\n\nStep 4: Locate Implementation Guide');
    console.log('────────────────────────────────────');
    
    const defaultGuidePath = path.resolve(
      __dirname,
      '..',
      '_mapping',
      productAbbreviation,
      '_run-prompts',
      `04d-${productAbbreviation}-implementation-guide_v1.md`
    );
    
    const guidePath = await getValidPath(
      'Enter path to implementation guide:',
      defaultGuidePath,
      true
    );
    
    console.log(`✓ Using guide: ${toDisplayPath(guidePath)}`);
    
    // Step 5: Get output path
    console.log('\n\nStep 5: Choose Output Location');
    console.log('───────────────────────────────');
    
    const defaultOutputPath = path.resolve(
      __dirname,
      '..',
      '_mapping',
      productAbbreviation,
      `04e-${productAbbreviation}-integrated-extension-spec_v1.md`
    );
    
    const outputPath = await getValidPath(
      'Enter path for integrated extension spec output:',
      defaultOutputPath,
      false
    );
    
    console.log(`✓ Output will be saved to: ${toDisplayPath(outputPath)}`);
    
    // Step 6: Process files
    console.log('\n\nStep 6: Process and Merge');
    console.log('─────────────────────────');
    
    console.log('📂 Reading input files...');
    const specContent = readFile(specPath);
    const inventoryContent = readFile(inventoryPath);
    const strategyContent = readFile(strategyPath);
    const guideContent = readFile(guidePath);
    
    console.log('🔍 Extracting sections from structured spec...');
    const sections = extractSections(specContent);
    console.log(`✓ Found ${sections.length} sections`);
    
    console.log('🔄 Transforming sections with integration knowledge...');
    const transformedSections = sections.map((section, index) => {
      console.log(`   Processing Section ${section.number}: ${section.title}`);
      return transformSection(section, inventoryContent, strategyContent, guideContent, projectName);
    });
    console.log('✓ All sections transformed');
    
    console.log('📝 Generating integrated specification...');
    let integratedSpec = generateHeader(projectName);
    
    for (const transformedSection of transformedSections) {
      integratedSpec += transformedSection;
    }
    
    integratedSpec += generateFooter();
    
    console.log('💾 Writing output file...');
    writeFile(outputPath, integratedSpec);
    
    // Summary
    console.log('\n\n╔════════════════════════════════════════════════════════════╗');
    console.log('║                    ✅ MERGE COMPLETE!                       ║');
    console.log('╚════════════════════════════════════════════════════════════╝\n');
    
    console.log('📋 Summary:');
    console.log('─────────');
    console.log(`Project:                ${projectName} (${productAbbreviation})`);
    console.log(`Sections Processed:     ${sections.length}`);
    console.log(`Output File:            ${toDisplayPath(outputPath)}`);
    console.log(`File Size:              ${(integratedSpec.length / 1024).toFixed(2)} KB`);
    
    console.log('\n\n📖 Next Steps:');
    console.log('─────────────');
    console.log('1. Review the integrated specification to ensure:');
    console.log('   - Infrastructure transformations are correct');
    console.log('   - All sections reference existing patterns');
    console.log('   - Integration notes are comprehensive');
    console.log('');
    console.log('2. Run the segmentation script to generate execution prompts:');
    console.log(`   node 04f-segment-integrated-spec_v2.js "${projectName}" ${productAbbreviation}`);
    console.log('');
    console.log('3. Execute prompts progressively to implement the module');
    console.log('');
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    if (error.stack) {
      console.error('\nStack trace:');
      console.error(error.stack);
    }
    process.exit(1);
  } finally {
    rl.close();
  }
}

// Run the script
main();
