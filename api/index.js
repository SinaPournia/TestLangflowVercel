import { v4 as uuidv4 } from 'uuid'; // Import the UUID generator

export default async function handler(req, res) {
  const apiKey = process.env.LANGFLOW_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'LANGFLOW_API_KEY environment variable not found.' });
  }

  // Generate a random session ID using uuid
  const sessionId = uuidv4();

  const payload = {
    "input_value": "hello world!",
    "output_type": "chat",
    "input_type": "chat",
    "session_id": sessionId // Use the dynamically generated session ID
  };

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      "x-api-key": apiKey
    },
    body: JSON.stringify(payload)
  };

  try {
    const response = await fetch('https://langflow.dev.aiprojectx.de/api/v1/run/31e780e0-3529-4e67-a60f-5f778a28e8b1', options);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch from Langflow API.' });
  }
}