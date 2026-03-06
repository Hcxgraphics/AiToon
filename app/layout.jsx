import { Providers } from "@/components/providers";
import "./globals.css";

export const metadata = {
  title: "AiToon",
  description: "A professional AI-powered comic creation studio. Chat with AI, design panels, write dialogue, and build your story.",
  openGraph: {
    title: "AI Comic Studio",
    description: "Create comics with AI assistance",
    type: "website",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
