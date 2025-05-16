import { v4 as uuidv4 } from 'uuid';

export default async function handler(req, res) {
  // ... (rest of your headers and OPTIONS handling) ...

  if (req.method === 'POST') {
    // ... (rest of your API key and payload construction) ...

    try {
      const response = await fetch(
        'https://langflow.dev.aiprojectx.de/api/v1/run/31e780e0-3529-4e67-a60f-5f778a28e8b1',
        options
      );
      const data = await response.json();
      console.log('Langflow Response Data:', data);

      let langflowOutput = null;
      if (data && data.outputs && data.outputs.length > 0 && data.outputs[0].outputs && data.outputs[0].outputs.length > 0) {
        langflowOutput = data.outputs[0].outputs[0]; // Extract the first output text
      }

      res.status(response.status).json({ output: langflowOutput }); // Send only the output

    } catch (error) {
      // ... (your error handling) ...
    }
  }
}