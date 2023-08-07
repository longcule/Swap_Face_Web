const axios = require('axios');

async function fetchData() {

  try {
    const response = await axios.get('http://127.0.0.1:5000', {
      headers: {
        Authorization: `Bearer`,
      },
      responseType: 'stream',
    });

    const stream = response.data;

    let data = '';
    stream.on('data', (chunk) => {
      data = '';
      data += chunk;
      console.log(data);
    });

    stream.on('end', () => {
    //   console.log(data);
      console.log("stream done");
    });
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

fetchData();
