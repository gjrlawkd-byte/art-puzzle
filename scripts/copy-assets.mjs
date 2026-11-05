// vite build 뒤에 작품 이미지와 데이터를 dist 로 복사한다 (런타임에 상대 경로로 불러옴)
import { cpSync, mkdirSync } from 'node:fs';

mkdirSync('dist/data', { recursive: true });
cpSync('art', 'dist/art', { recursive: true, filter: src => !src.endsWith('meta.json') });
cpSync('data/paintings.json', 'dist/data/paintings.json');
console.log('copied art/ and data/paintings.json to dist/');
