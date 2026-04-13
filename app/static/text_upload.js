
export async function sendPrompt({ prompt, model, session_id, guestId }) {
  const response = await fetch('/prompt', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'x-guest-id': guestId,
    },
    body: JSON.stringify({
      prompt,
      model,
      session_id,
    }),
  });

  if (!response.ok) {
    throw new Error("Request failed");
  }

  return response.json();
}