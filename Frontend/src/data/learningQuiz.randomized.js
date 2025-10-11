import raw from './learningQuiz.js';
import { randomizeLearningQuiz } from '@/utils/quiz-shuffle.js';

const learningQuiz = randomizeLearningQuiz(raw);
export default learningQuiz;
