export async function sendPrompt({ prompt, model, session_id, guestId }) {
  const response = await fetch('/prompt', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'x-guest-id': guestId,
    },
    body: JSON.stringify({ prompt, model, session_id }),
  });

  const data = await response.json();  // always read the body

  if (!response.ok) {
    // Attach status + server message to the error so the caller can use it
    const err = new Error(data.message || "Request failed");
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
}