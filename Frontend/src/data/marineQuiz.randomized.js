import raw from './marineQuiz.js';
import { randomizeMarineQuiz } from '@/utils/quiz-shuffle.js';

const marineQuiz = randomizeMarineQuiz(raw);
export default marineQuiz;
