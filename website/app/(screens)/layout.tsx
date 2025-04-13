"use client";

import { SocketProvider } from '../socket';

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SocketProvider>
      {children}
    </SocketProvider>
  );
}