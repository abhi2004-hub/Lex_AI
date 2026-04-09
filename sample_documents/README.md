# Sample Legal Documents for LexAI Testing

This directory contains sample legal documents to test your LexAI Legal Document Intelligence Platform.

## Available Documents

### 1. **Employment Contract** (`employment_contract.txt`)
- **Type**: Employment Agreement
- **Key Clauses**: Compensation, confidentiality, non-compete, liability limitation
- **Risk Level**: Medium-High (due to restrictive non-compete and liability limitations)
- **Size**: ~2 pages
- **Perfect for testing**: Clause extraction, risk assessment, employment law analysis

### 2. **Service Agreement** (`service_agreement.txt`)
- **Type**: B2B Service Contract
- **Key Clauses**: Payment terms, intellectual property, liability, warranties
- **Risk Level**: Medium (balanced terms with some limitations)
- **Size**: ~3 pages
- **Perfect for testing**: Business contract analysis, IP clause detection

### 3. **Non-Disclosure Agreement** (`nda_agreement.txt`)
- **Type**: Confidentiality Agreement
- **Key Clauses**: Confidential information, remedies, exclusions
- **Risk Level**: Low-Medium (standard NLA terms)
- **Size**: ~2 pages
- **Perfect for testing**: Confidentiality clause detection, data protection analysis

### 4. **Commercial Lease Agreement** (`lease_agreement.txt`)
- **Type**: Real Estate Lease
- **Key Clauses**: Rent, use restrictions, insurance, default provisions
- **Risk Level**: Medium (commercial lease with standard protections)
- **Size**: ~3 pages
- **Perfect for testing**: Real estate document analysis, financial clause detection

## Testing Recommendations

### 🎯 **Start With These Documents**

1. **First Test**: `employment_contract.txt`
   - Contains diverse clause types
   - Good mix of risk levels
   - Clear section numbering

2. **Second Test**: `service_agreement.txt`
   - Business-focused content
   - Intellectual property clauses
   - Payment and liability terms

3. **Advanced Test**: `lease_agreement.txt`
   - Longer document
   - Complex legal language
   - Multiple risk factors

### 🔍 **What to Look For**

**Clause Extraction**:
- Confidentiality clauses
- Termination provisions
- Liability limitations
- Payment terms
- Non-compete agreements

**Risk Assessment**:
- High-risk: Unlimited liability, restrictive non-competes
- Medium-risk: Standard termination clauses, payment penalties
- Low-risk: Basic confidentiality, standard warranties

**AI Explanations**:
- SHAP values highlighting key terms
- LIME explanations for risk classifications
- Confidence scores for clause identification

### 📊 **Expected Results**

Each document should provide:
- **15-25 extracted clauses**
- **Risk distribution**: 60% low, 25% medium, 15% high
- **Processing time**: 2-5 seconds
- **Confidence scores**: 70-95% average

### 🚀 **How to Use**

1. **Upload**: Go to http://localhost:3000
2. **Drag & Drop**: Any of these .txt files
3. **Select Analysis Type**: "Detailed" for best results
4. **Review Results**: Check dashboard for insights

### 💡 **Testing Tips**

- **Compare Results**: Upload the same document multiple times to test consistency
- **Different Analysis Types**: Try "Quick" vs "Detailed" analysis
- **Error Handling**: Try uploading unsupported file types
- **Performance**: Test with multiple documents simultaneously

### 🎓 **Educational Value**

These documents demonstrate:
- **Real-world legal language**
- **Standard contract structures**
- **Common legal clauses and provisions**
- **Risk factors in business agreements**
- **Professional legal document formatting**

---

**Perfect for demonstrating your LexAI platform to professors, evaluators, or potential investors!** 🎓

Each document showcases different aspects of your AI capabilities and provides realistic test cases for your legal intelligence system.
