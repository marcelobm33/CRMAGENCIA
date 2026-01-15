import { Suspense } from 'react';
import PublicRoiClient from './PublicRoiClient';

export default function PublicRoiPage() {
  return (
    <Suspense
      fallback={
        <div className="bg-white rounded-2xl border p-6">
          <p className="text-gray-600">Carregando…</p>
        </div>
      }
    >
      <PublicRoiClient />
    </Suspense>
  );
}

