/**
 * Integration Prompt Generator (v2)
 * 
 * Purpose: Generate a custom integration prompt for a specific project by combining
 *          the generic meta-prompt template with project-specific file paths.
 * 
 * Inputs:
 *   - Generic meta-prompt template (04d-integrate-existing-codebase_v2.md)
 *   - Project-specific paths (structured spec, codebase, output directory)
 * 
 * Output:
 *   - Custom integration prompt ready to execute
 *   - This prompt, when executed by an AI, will generate three documents:
 *     1. Infrastructure Inventory
 *     2. Extension Strategy
 *     3. Implementation Guide
 * 
 * Usage:
 *   node 04e-merge-integration-spec_v2.js \
 *     --template "path/to/04d-integrate-existing-codebase_v2.md" \
 *     --spec "path/to/04c-pipeline-structured-from-wireframe_v1.md" \
 *     --codebase "path/to/src/" \
 *     --output-dir "path/to/output/" \
 *     --prompt-output "path/to/04e-custom-integration-prompt_v1.md"
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    const value = args[i + 1];
    parsed[key] = value;
  }
  
  return parsed;
}

/**
 * Read file content
 */
function readFile(filePath) {
  try {
    const absolutePath = path.resolve(filePath);
    if (!fs.existsSync(absolutePath)) {
      throw new Error(`File not found: ${absolutePath}`);
    }
    return fs.readFileSync(absolutePath, 'utf-8');
  } catch (error) {
    console.error(`Error reading file ${filePath}:`, error.message);
    process.exit(1);
  }
}

/**
 * Write file content
 */
function writeFile(filePath, content) {
  try {
    const absolutePath = path.resolve(filePath);
    const dir = path.dirname(absolutePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(absolutePath, content, 'utf-8');
    console.log(`✅ Written: ${absolutePath}`);
  } catch (error) {
    console.error(`Error writing file ${filePath}:`, error.message);
    process.exit(1);
  }
}

/**
 * Resolve path to absolute and normalize
 */
function resolvePath(inputPath) {
  return path.resolve(inputPath).replace(/\\/g, '/');
}

/**
 * Get project name from spec filename or path
 */
function extractProjectName(specPath) {
  const basename = path.basename(specPath, '.md');
  // Extract meaningful name from filename like "04c-pipeline-structured-from-wireframe_v1"
  const match = basename.match(/04c-(.+?)(?:_v\d+)?$/);
  if (match) {
    // Convert kebab-case to Title Case
    return match[1]
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  return 'New Module';
}

/**
 * Generate metadata section for the custom prompt
 */
function generateMetadata(specPath, codebasePath, outputDir) {
  const date = new Date().toISOString().split('T')[0];
  const projectName = extractProjectName(specPath);
  
  return `# Codebase Extension Analysis - ${projectName}

**Generated:** ${date}
**Template:** 04d-integrate-existing-codebase_v2.md
**Purpose:** Generate extension documentation for implementing ${projectName} as a new module

---

## PROJECT-SPECIFIC PATHS

**Structured Specification:**
\`${resolvePath(specPath)}\`

**Existing Codebase:**
\`${resolvePath(codebasePath)}\`

**Output Directory:**
\`${resolvePath(outputDir)}\`

---

`;
}

/**
 * Replace placeholders in template with actual values
 */
function replacePlaceholders(template, specPath, codebasePath, outputDir) {
  const resolvedSpecPath = resolvePath(specPath);
  const resolvedCodebasePath = resolvePath(codebasePath);
  const resolvedOutputDir = resolvePath(outputDir);
  
  // Replace all placeholder patterns
  let customPrompt = template;
  
  // Replace placeholders with actual paths
  customPrompt = customPrompt.replace(/\{\{STRUCTURED_SPEC_PATH\}\}/g, resolvedSpecPath);
  customPrompt = customPrompt.replace(/\{\{CODEBASE_PATH\}\}/g, resolvedCodebasePath);
  customPrompt = customPrompt.replace(/\{\{OUTPUT_PATH\}\}/g, resolvedOutputDir);
  
  return customPrompt;
}

/**
 * Add execution instructions to the custom prompt
 */
function addExecutionInstructions(outputDir) {
  return `

---

## EXECUTION INSTRUCTIONS

When you execute this prompt, you will generate THREE documents in the output directory:

1. **\`04d-infrastructure-inventory_v1.md\`**
   - Complete inventory of existing codebase infrastructure
   - What exists and is available to use
   - Expected size: ~2,000-3,000 lines

2. **\`04d-extension-strategy_v1.md\`**
   - Features extracted from spec (ignoring tech choices)
   - How new module uses existing infrastructure
   - What new things need to be created
   - Expected size: ~1,500-2,500 lines

3. **\`04d-implementation-guide_v1.md\`**
   - Exact step-by-step implementation instructions
   - Code examples using existing patterns
   - Implementation checklist
   - Expected size: ~2,000-4,000 lines

**Total Expected Output:** ~5,500-9,500 lines of comprehensive extension documentation

---

## HOW TO PROCEED

1. **Read the Structured Specification** to understand WHAT FEATURES need to be built
2. **Analyze the Existing Codebase** to understand WHAT INFRASTRUCTURE exists
3. **Generate the THREE documents** following the templates and guidelines in this prompt
4. **Ensure EXTENSION framing** throughout - this is NOT integration, it's adding a module
5. **Focus on REUSE** - maximize use of existing infrastructure

**Remember:** The spec describes FEATURES. The codebase provides INFRASTRUCTURE. Your job is to document HOW TO IMPLEMENT THE FEATURES USING THE INFRASTRUCTURE.

---

**Ready to begin? Start with Phase 1: Infrastructure Inventory.**

`;
}

/**
 * Validate required files exist
 */
function validateInputs(templatePath, specPath, codebasePath) {
  const errors = [];
  
  // Check template
  const resolvedTemplatePath = path.resolve(templatePath);
  if (!fs.existsSync(resolvedTemplatePath)) {
    errors.push(`Template not found: ${resolvedTemplatePath}`);
  }
  
  // Check spec
  const resolvedSpecPath = path.resolve(specPath);
  if (!fs.existsSync(resolvedSpecPath)) {
    errors.push(`Structured spec not found: ${resolvedSpecPath}`);
  }
  
  // Check codebase directory
  const resolvedCodebasePath = path.resolve(codebasePath);
  if (!fs.existsSync(resolvedCodebasePath)) {
    errors.push(`Codebase directory not found: ${resolvedCodebasePath}`);
  } else if (!fs.statSync(resolvedCodebasePath).isDirectory()) {
    errors.push(`Codebase path is not a directory: ${resolvedCodebasePath}`);
  }
  
  return errors;
}

// ============================================================================
// MAIN FUNCTION
// ============================================================================

function main() {
  console.log('🚀 Integration Prompt Generator v2\n');
  
  // Parse arguments
  const args = parseArgs();
  
  // Validate required arguments
  if (!args.template || !args.spec || !args.codebase || !args['output-dir'] || !args['prompt-output']) {
    console.error('❌ Missing required arguments\n');
    console.error('Usage: node 04e-merge-integration-spec_v2.js \\');
    console.error('    --template "path/to/04d-integrate-existing-codebase_v2.md" \\');
    console.error('    --spec "path/to/04c-pipeline-structured-from-wireframe_v1.md" \\');
    console.error('    --codebase "path/to/src/" \\');
    console.error('    --output-dir "path/to/output/" \\');
    console.error('    --prompt-output "path/to/04e-custom-integration-prompt_v1.md"\n');
    console.error('Arguments:');
    console.error('  --template      Path to generic meta-prompt template (v2)');
    console.error('  --spec          Path to structured specification');
    console.error('  --codebase      Path to existing codebase directory');
    console.error('  --output-dir    Path to output directory for generated documents');
    console.error('  --prompt-output Path to save the custom integration prompt\n');
    process.exit(1);
  }
  
  // Validate inputs
  console.log('🔍 Validating input files...\n');
  const errors = validateInputs(args.template, args.spec, args.codebase);
  
  if (errors.length > 0) {
    console.error('❌ Validation errors:\n');
    errors.forEach(error => console.error(`   - ${error}`));
    console.error('');
    process.exit(1);
  }
  
  console.log('✅ All input files validated\n');
  
  // Read template
  console.log('📂 Reading generic meta-prompt template...\n');
  const template = readFile(args.template);
  console.log(`✅ Template: ${path.resolve(args.template)}`);
  console.log(`   Size: ${(template.length / 1024).toFixed(2)} KB\n`);
  
  // Generate metadata
  console.log('🔧 Generating project-specific metadata...\n');
  const metadata = generateMetadata(args.spec, args.codebase, args['output-dir']);
  console.log('✅ Metadata generated\n');
  
  // Replace placeholders
  console.log('🔄 Replacing placeholders with project paths...\n');
  const customPrompt = replacePlaceholders(template, args.spec, args.codebase, args['output-dir']);
  console.log('✅ Placeholders replaced:\n');
  console.log(`   {{STRUCTURED_SPEC_PATH}} → ${resolvePath(args.spec)}`);
  console.log(`   {{CODEBASE_PATH}}        → ${resolvePath(args.codebase)}`);
  console.log(`   {{OUTPUT_PATH}}          → ${resolvePath(args['output-dir'])}\n`);
  
  // Add execution instructions
  console.log('📝 Adding execution instructions...\n');
  const executionInstructions = addExecutionInstructions(args['output-dir']);
  console.log('✅ Instructions added\n');
  
  // Combine all parts
  console.log('🔨 Assembling custom integration prompt...\n');
  const finalPrompt = metadata + customPrompt + executionInstructions;
  console.log('✅ Custom prompt assembled\n');
  console.log(`   Total size: ${(finalPrompt.length / 1024).toFixed(2)} KB\n`);
  
  // Write output
  console.log('💾 Writing custom integration prompt...\n');
  writeFile(args['prompt-output'], finalPrompt);
  
  // Summary
  console.log('\n✅ PROMPT GENERATION COMPLETE!\n');
  console.log('📊 Summary:');
  console.log(`   - Template used: ${path.basename(args.template)}`);
  console.log(`   - Spec: ${path.basename(args.spec)}`);
  console.log(`   - Codebase: ${path.basename(args.codebase)}`);
  console.log(`   - Output prompt: ${path.resolve(args['prompt-output'])}`);
  console.log(`   - Prompt size: ${(finalPrompt.length / 1024).toFixed(2)} KB\n`);
  
  console.log('🎯 Next steps:\n');
  console.log('   1. Review the generated prompt:');
  console.log(`      ${path.resolve(args['prompt-output'])}\n`);
  console.log('   2. Execute the prompt using an AI assistant to generate:');
  console.log(`      - ${path.resolve(args['output-dir'])}/04d-infrastructure-inventory_v1.md`);
  console.log(`      - ${path.resolve(args['output-dir'])}/04d-extension-strategy_v1.md`);
  console.log(`      - ${path.resolve(args['output-dir'])}/04d-implementation-guide_v1.md\n`);
  console.log('   3. Once you have those three documents, run the segmentation script:');
  console.log(`      node 04f-segment-integrated-spec_v1.js --input "..." --output-dir "..."\n`);
}

// ============================================================================
// ENTRY POINT
// ============================================================================

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error('\n❌ ERROR:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

module.exports = { 
  replacePlaceholders, 
  generateMetadata, 
  addExecutionInstructions,
  extractProjectName,
  resolvePath
};
