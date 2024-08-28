"use client";
import { useState } from "react";

export default function Chat() {
    const [messages, setMessages] = useState<{ id: string; role: string; content: string }[]>([]);
    const [input, setInput] = useState("");
    const [isUserPrompt, setIsUserPrompt] = useState(false);

    const handleSubmitForm = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (input.trim() !== "") {
            setIsUserPrompt(true);

            // Append the user's message to the message list
            setMessages((prev) => [
                ...prev,
                { id: `user-${Date.now()}`, role: "user", content: input },
            ]);

            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    messages: [
                        ...messages,
                        { id: `user-${Date.now()}`, role: "user", content: input },
                    ],
                }),
            });

            const data = await response.json();

            // Append the assistant's message to the message list
            setMessages((prev) => [
                ...prev,
                { id: `assistant-${Date.now()}`, role: "assistant", content: data.text },
            ]);

            setInput("");
            setIsUserPrompt(false);
        }
    };

    return (
        <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
            {messages.map((message) => (
                <div
                    key={message.id}
                    className="whitespace-pre-wrap"
                    style={{ color: message.role === "user" ? "black" : "green" }}
                >
                    <strong>{`${message.role}: `}</strong>
                    {message.content}
                    <br />
                    <br />
                </div>
            ))}
            <form onSubmit={handleSubmitForm}>
                <input
                    className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
                    value={input}
                    placeholder="Say something..."
                    onChange={(e) => setInput(e.target.value)}
                />
            </form>
        </div>
    );
}
