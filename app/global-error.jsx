'use client';

export default function GlobalError({ error, reset }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Something went wrong</h2>
          <button
            onClick={() => reset()}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md"
          >
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
