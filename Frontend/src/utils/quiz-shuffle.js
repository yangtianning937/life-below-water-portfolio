// Fisher–Yates 洗牌 + 重映射 a/b/c… 并重算 answer
const LETTERS = 'abcdefghijklmnopqrstuvwxyz'.split('');

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = (Math.random() * (i + 1)) | 0;
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/**
 * 对 MCQ/PIC 题乱序选项并重算正确答案键。
 * - 对 True/False（t/f）与配对题不改键位（如需随机显示顺序，可在渲染层使用 getTFOptionsForRender）。
 */
export function shuffleQuestionOptions(q) {
  if (!q || !q.options || q.options.length <= 1) return q;

  const isTF =
    q.type === 'tf' ||
    q.options.every(o => {
      const k = String(o.key).toLowerCase();
      return k === 't' || k === 'f' || k === 'true' || k === 'false';
    });

  // TF 或 match 题不动
  if (isTF || q.type === 'match') return q;

  // 标记原正确项
  const tagged = q.options.map(opt => ({
    ...opt,
    __correct__: String(opt.key) === String(q.answer),
  }));

  // 洗牌并重新分配 a/b/c/d...
  const shuffled = shuffle(tagged);
  const remapped = shuffled.map((opt, idx) => ({
    ...opt,
    key: LETTERS[idx] ?? String(idx),
  }));

  // 新答案：找到被标记为正确的那一项
  const correct = remapped.find(o => o.__correct__ === true);
  const newAnswer = correct ? correct.key : remapped[0].key;

  // 清理标记
  const options = remapped.map(({ __correct__, ...rest }) => rest);

  return { ...q, options, answer: newAnswer };
}

/** learningQuiz.js 结构通常为：{ m1:[], m2:[], m3:[] }（也兼容数组） */
export function randomizeLearningQuiz(raw) {
  if (Array.isArray(raw)) return raw.map(q => shuffleQuestionOptions(q));
  const out = {};
  Object.keys(raw || {}).forEach(k => {
    out[k] = (raw[k] || []).map(q => shuffleQuestionOptions(q));
  });
  return out;
}

/** marineQuiz.js 结构：{ mcq:[], tf:[], match:[], pic:[] }（字段缺失也安全处理） */
export function randomizeMarineQuiz(raw) {
  return {
    mcq: (raw?.mcq || []).map(q => shuffleQuestionOptions({ ...q, type: 'mcq' })),
    tf: raw?.tf || [],       // 不改键位（t/f）
    match: raw?.match || [], // 不动
    pic: (raw?.pic || []).map(q => shuffleQuestionOptions({ ...q, type: 'pic' })),
  };
}

/** （可选）让 True/False 在渲染层随机“显示顺序”，但不改答案键 */
export function getTFOptionsForRender(options = []) {
  if (options.length !== 2) return options;
  return Math.random() > 0.5 ? [options[1], options[0]] : options.slice();
}
