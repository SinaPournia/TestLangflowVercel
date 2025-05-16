import { v4 as uuidv4 } from 'uuid';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-api-key');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const apiKey = process.env.LANGFLOW_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: 'LANGFLOW_API_KEY environment variable not found.' });
    }

    try {
      const body = JSON.parse(req.body);
      const userMessage = body.input_value; // Extract the user's message

      const sessionId = uuidv4();

      const payload = {
        "input_value": userMessage, // Use the user's message here
        "output_type": "chat",
        "input_type": "chat",
        "session_id": sessionId
      };

      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "x-api-key": apiKey
        },
        body: JSON.stringify(payload)
      };

      const response = await fetch('https://langflow.dev.aiprojectx.de/api/v1/run/31e780e0-3529-4e67-a60f-5f778a28e8b1', options);
      const data = await response.json();
      res.status(response.status).json(data);

    } catch (error) {
      console.error('Error processing request:', error);
      res.status(500).json({ error: 'Failed to process the request.' });
    }
  } else {
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}