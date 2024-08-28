export const runtime = "edge";
import { Message } from "ai";  // Adjust this according to the actual package

export async function POST(req: Request) {
    const { messages }: { messages: Message[] } = await req.json();

    // Extract the user's message
    const userMessage = messages[messages.length - 1].content;

    // Send a request to the Flask API
    const response = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: userMessage }),
    });

    const data = await response.json();

    // Log the response for debugging
    console.log("Response from Flask API:", data.response);

    // Return the response to the frontend
    return new Response(JSON.stringify({ text: data.response }), {
        headers: { "Content-Type": "application/json" },
    });
}