// backend/test.js
const axios = require('axios');

const BASE_URL = 'http://localhost:3000';

async function testEndpoints() {
  try {
    console.log('🧪 Testing backend endpoints...\n');

    // Test health endpoint
    console.log('1. Testing /health endpoint...');
    const healthResponse = await axios.get(`${BASE_URL}/health`);
    console.log('✅ Health check passed:', healthResponse.data);

    // Test root endpoint
    console.log('\n2. Testing / endpoint...');
    const rootResponse = await axios.get(`${BASE_URL}/`);
    console.log('✅ Root endpoint passed:', rootResponse.data);

    // Test API endpoint
    console.log('\n3. Testing /api/test endpoint...');
    const apiResponse = await axios.get(`${BASE_URL}/api/test`);
    console.log('✅ API test endpoint passed:', apiResponse.data);

    console.log('\n🎉 All tests passed! Backend is working correctly.');
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  testEndpoints();
}

module.exports = { testEndpoints }; 