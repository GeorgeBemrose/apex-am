import { useState } from "react";

export default function WaitlistForm() {
    const [email, setEmail] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log(`Email submitted: ${email}`);
        setEmail(""); // Clear the input field after submission
    };

    return (
        <div className="bg-gray-100 p-6 rounded-lg shadow-md max-w-md mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 text-center mb-4">Join the Waitlist</h2>
            <p className="text-gray-600 text-center mb-6">
                Be the first to experience the future of accounting AI.
            </p>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                    Join Waitlist
                </button>
            </form>
        </div>
    );
}