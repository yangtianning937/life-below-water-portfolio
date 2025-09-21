export default {
  m1: [
    {
      key: 'm1-q1',
      text: 'What does an ecosystem mean in the ocean?',
      options: [
        { key: 'a', label: 'A single fish swimming alone' },
        { key: 'b', label: 'A big neighborhood where animals, plants, and tiny creatures live together' },
        { key: 'c', label: 'A sandy beach without animals' },
      ],
      answer: 'b',
      correct: 'Yes! An ecosystem is like a big neighborhood where everything depends on each other.',
      incorrect: 'Not quite—it means many animals, plants, and small creatures living together.',
    },
    {
      key: 'm1-q2',
      text: '“Seagrass provides food and shelter for fish.”',
      options: [
        { key: 't', label: 'True' },
        { key: 'f', label: 'False' },
      ],
      answer: 't',
      correct: 'Correct! Seagrass meadows are important ocean homes.',
      incorrect: 'Oops—it’s true. Seagrass gives fish food and shelter.',
    },
  ],
  m2: [
    {
      key: 'm2-q3',
      text: 'This beach is famous for colorful bathing boxes.',
      // 可选图片：把文件放到 Frontend/public/quiz/brighton_boxes.jpg
      image: '/learning/beaches/brighton_bathing_boxes.jpg',
      options: [
        { key: 'a', label: 'Brighton Beach' },
        { key: 'b', label: 'St Kilda Beach' },
        { key: 'c', label: 'Sorrento Beach' },
      ],
      answer: 'a',
      correct: 'Yes! Brighton Beach is well known for its colorful bathing boxes.',
      incorrect: 'Not this one—it’s Brighton Beach, famous for the bathing boxes.',
    },
    {
      key: 'm2-q4',
      text: 'At St Kilda Beach, what special animals can you see?',
      options: [
        { key: 'a', label: 'Penguins' },
        { key: 'b', label: 'Sharks' },
        { key: 'c', label: 'Seals' },
      ],
      answer: 'a',
      correct: 'Correct! Little penguins live at St Kilda Beach.',
      incorrect: 'Nope—it’s penguins. You can spot them at St Kilda Beach.',
    },
  ],
  m3: [
    {
      key: 'm3-q5',
      text: '“If one part of the marine food chain is missing, the whole chain can be affected.”',
      options: [
        { key: 't', label: 'True' },
        { key: 'f', label: 'False' },
      ],
      answer: 't',
      correct: 'Yes! That’s why we need good water quality for all animals to survive.',
      incorrect: 'Wrong—it’s true. The whole chain depends on each part.',
    },
    {
      key: 'm3-q6',
      text: 'Match the beach to what it is famous for (choose the correct set).',
      // 为了复用现有多选按钮，把配对题改成“选正确的一组配对”
      options: [
        { key: 'a', label: 'St Kilda→Penguins; Dromana→Paddle boarding; Sorrento→Rock pools' },
        { key: 'b', label: 'St Kilda→Seals; Dromana→Surfing; Sorrento→Penguins' },
        { key: 'c', label: 'St Kilda→Bathing boxes; Dromana→Rock pools; Sorrento→Paddle boarding' },
      ],
      answer: 'a',
      correct: 'Perfect! You matched beaches with their special features.',
      incorrect: 'Not quite—St Kilda = penguins, Dromana = paddle boarding, Sorrento = rock pools.',
    },
    {
      key: 'm3-q7',
      text: 'What’s one way to stay safe at the beach?',
      options: [
        { key: 'a', label: 'Swim between the red and yellow flags' },
        { key: 'b', label: 'Swim anywhere, even far away' },
        { key: 'c', label: 'Swim alone' },
      ],
      answer: 'a',
      correct: 'Correct! Swimming between the flags keeps you safe.',
      incorrect: 'Not safe—it’s best to swim between the red and yellow flags.',
    },
  ],
}
