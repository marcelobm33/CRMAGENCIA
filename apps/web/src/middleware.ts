import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

const TOKEN = process.env.PUBLIC_REPORT_TOKEN;

export function middleware(req: NextRequest) {
  const { pathname, searchParams } = req.nextUrl;

  const isPublicRoi = pathname.startsWith('/publico/roi');
  const isPublicJson = pathname === '/public-report.json';
  if (!isPublicRoi && !isPublicJson) return NextResponse.next();

  // "Somente quem tem o link": exige ?t=TOKEN (e retorna 404 quando inválido).
  // Observação: isso não substitui autenticação real; é um bloqueio simples por token.
  if (TOKEN) {
    const t = searchParams.get('t');
    if (!t || t !== TOKEN) return new NextResponse('Not Found', { status: 404 });
  }

  const res = NextResponse.next();
  res.headers.set('x-robots-tag', 'noindex, nofollow');
  return res;
}

export const config = {
  matcher: ['/publico/roi/:path*', '/public-report.json'],
};

