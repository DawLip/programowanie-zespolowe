import { Inter } from 'next/font/google'
import type { Metadata } from "next";
import "./globals.css";

const roboto = Inter({
  weight: ['400', '600','700'],
  style: ['normal'],
  subsets: ['latin'],
})
export const metadata: Metadata = {
  title: "ChatNow"
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
