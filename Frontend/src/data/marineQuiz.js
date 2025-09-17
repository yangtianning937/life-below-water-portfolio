// Frontend/src/data/marineQuiz.js
// 四类题：mcq / tf / match / pic
// 约定：
// - MCQ: 每个选项 { key, name, img }，题目可带 promptImg（可选）
// - TF:  answer: 't' | 'f'
// - MATCH: { left:[{key,label,img}], right:[{key,label}], answer:{ [leftKey]: rightKey } }
// - PIC:  题干一张图片 image，选项为纯文本 name

const mcq = [
  {
    key: 'mcq-turtle-1',
    type: 'mcq',
    text: 'What is this animal?',
    promptImg: '/quiz/pics/sea_turtle.jpg',           // 题图（可选）
    options: [
      { key: 'a', name: 'Dolphin',    img: '/quiz/animals/dolphin.jpg' },
      { key: 'b', name: 'Sea Turtle', img: '/quiz/animals/sea_turtle.jpg' }, // ✅
      { key: 'c', name: 'Shark',      img: '/quiz/animals/shark.jpg' },
    ],
    answer: 'b',
    correct: '🎉 Yes! That’s a Sea Turtle. They travel far and need clean water.',
    incorrect: '❌ Not quite—this is a Sea Turtle.',
  },
  {
    key: 'mcq-dolphin-comm',
    type: 'mcq',
    text: 'Which animal uses sounds to talk with friends?',
    options: [
      { key: 'a', name: 'Dolphin', img: '/quiz/animals/dolphin.jpg' }, // ✅
      { key: 'b', name: 'Octopus', img: '/quiz/animals/octopus.jpg' },
      { key: 'c', name: 'Crab',    img: '/quiz/animals/crab.jpg' },
    ],
    answer: 'a',
    correct: '✅ Correct! Dolphins use clicks and whistles to communicate.',
    incorrect: '❌ Oops—it’s the Dolphin.',
  },
  {
    key: 'mcq-clownfish-1',
    type: 'mcq',
    text: 'Which fish lives safely in sea anemones?',
    options: [
      { key: 'a', name: 'Clownfish', img: '/quiz/animals/clownfish.jpg' }, // ✅
      { key: 'b', name: 'Seahorse',  img: '/quiz/animals/seahorse.jpg' },
      { key: 'c', name: 'Tuna',      img: '/quiz/animals/tuna.jpg' },
    ],
    answer: 'a',
    correct: '🎉 Great! Clownfish hide in sea anemones.',
    incorrect: '❌ Not this one—it’s the Clownfish.',
  },
  {
    key: 'mcq-seagrass',
    type: 'mcq',
    text: 'What grows underwater and makes oxygen for fish?',
    options: [
      { key: 'a', name: 'Seagrass', img: '/quiz/animals/seagrass.jpg' }, // ✅ 可用示意图
      { key: 'b', name: 'Cactus',   img: '/quiz/animals/cactus.jpg' },
      { key: 'c', name: 'Bamboo',   img: '/quiz/animals/bamboo.jpg' },
    ],
    answer: 'a',
    correct: '✅ Yes! Seagrass meadows are the ocean’s lungs.',
    incorrect: '❌ Nope—it’s Seagrass.',
  },
  {
    key: 'mcq-crab-legs',
    type: 'mcq',
    text: 'Which one has 10 legs and walks sideways?',
    options: [
      { key: 'a', name: 'Crab',     img: '/quiz/animals/crab.jpg' }, // ✅
      { key: 'b', name: 'Starfish', img: '/quiz/animals/starfish.jpg' },
      { key: 'c', name: 'Seal',     img: '/quiz/animals/seal.jpg' },
    ],
    answer: 'a',
    correct: '✅ Correct! Crabs scuttle sideways.',
    incorrect: '❌ Close—it’s the Crab.',
  },
];

const tf = [
  {
    key: 'tf-plastic-turtle',
    type: 'tf',
    text: '“Plastic bags floating in the ocean can look like food to turtles.”',
    answer: 't',
    correct: 'Yes! Turtles mistake them for jellyfish.',
    incorrect: 'Incorrect—it’s true. Plastic is dangerous.',
  },
  {
    key: 'tf-coral-forest',
    type: 'tf',
    text: '“Coral reefs are called the rainforests of the sea.”',
    answer: 't',
    correct: 'Correct! Coral reefs are full of life.',
    incorrect: 'Not quite—this is true.',
  },
  {
    key: 'tf-rubbish-helps',
    type: 'tf',
    text: '“Throwing rubbish in the ocean helps fish.”',
    answer: 'f',
    correct: 'Correct! Rubbish hurts fish.',
    incorrect: 'Wrong—it’s false.',
  },
  {
    key: 'tf-seahorse-fish',
    type: 'tf',
    text: '“Seahorses are fish.”',
    answer: 't',
    correct: 'Yes! Seahorses are small fish.',
    incorrect: 'Incorrect—they really are fish.',
  },
  {
    key: 'tf-dolphin-mammal',
    type: 'tf',
    text: '“Dolphins are fish, not mammals.”',
    answer: 'f',
    correct: 'Correct! Dolphins are mammals.',
    incorrect: 'No—they are mammals, not fish.',
  },
  {
    key: 'tf-clean-beach',
    type: 'tf',
    text: '“Keeping beaches clean helps people and sea life.”',
    answer: 't',
    correct: 'Yes! Clean beaches help everyone.',
    incorrect: 'Wrong—it’s true.',
  },
];

const match = [
  {
    key: 'match-dolphin-jellyfish-clownfish',
    type: 'match',
    text: 'Match each animal to its trait.',
    left: [
      { key: 'dolphin',   label: 'Dolphin',   img: '/quiz/animals/dolphin.jpg' },
      { key: 'jellyfish', label: 'Jellyfish', img: '/quiz/animals/jellyfish.jpg' },
      { key: 'clownfish', label: 'Clownfish', img: '/quiz/animals/clownfish.jpg' },
    ],
    right: [
      { key: 'talk',   label: 'Use sounds to talk' },
      { key: 'soft',   label: 'Soft body, no bones' },
      { key: 'anem',   label: 'Lives in sea anemones' },
    ],
    answer: { dolphin: 'talk', jellyfish: 'soft', clownfish: 'anem' },
    correct: 'Perfect! You matched them all.',
    incorrect: 'Not quite—dolphins talk, clownfish hide in anemones, jellyfish are soft-bodied.',
  },
  {
    key: 'match-turtle-crab-whale',
    type: 'match',
    text: 'Match each animal to its trait.',
    left: [
      { key: 'turtle', label: 'Sea Turtle', img: '/quiz/animals/sea_turtle.jpg' },
      { key: 'crab',   label: 'Crab',       img: '/quiz/animals/crab.jpg' },
      { key: 'whale',  label: 'Whale',      img: '/quiz/animals/blue_whale.jpg' },
    ],
    right: [
      { key: 'migrate', label: 'Travels long distances' },
      { key: 'side',    label: 'Walks sideways' },
      { key: 'big',     label: 'Biggest mammal in the sea' },
    ],
    answer: { turtle: 'migrate', crab: 'side', whale: 'big' },
    correct: 'Great match!',
    incorrect: 'Turtles migrate, crabs walk sideways, whales are giants.',
  },
  {
    key: 'match-seahorse-starfish-shark',
    type: 'match',
    text: 'Match each animal to its trait.',
    left: [
      { key: 'seahorse', label: 'Seahorse', img: '/quiz/animals/seahorse.jpg' },
      { key: 'starfish', label: 'Starfish', img: '/quiz/animals/starfish.jpg' },
      { key: 'shark',    label: 'Shark',    img: '/quiz/animals/shark.jpg' },
    ],
    right: [
      { key: 'dad',  label: 'Dads carry the babies' },
      { key: 'arm',  label: 'Can grow back an arm' },
      { key: 'top',  label: 'Top hunter, balances ocean' },
    ],
    answer: { seahorse: 'dad', starfish: 'arm', shark: 'top' },
    correct: 'Correct! Amazing facts.',
    incorrect: 'Seahorses dads carry babies; starfish regrow arms; sharks are top predators.',
  },
];

const pic = [
  {
    key: 'pic-clownfish',
    type: 'pic',
    text: 'What is this fish?',
    image: '/quiz/pics/clownfish.jpg',
    options: [
      { key: 'a', name: 'Clownfish' }, // ✅
      { key: 'b', name: 'Starfish' },
      { key: 'c', name: 'Seahorse' },
    ],
    answer: 'a',
    correct: 'Yes! Clownfish live in anemones.',
    incorrect: 'Not quite—it’s a Clownfish.',
  },
  {
    key: 'pic-turtle',
    type: 'pic',
    text: 'What is this?',
    image: '/quiz/pics/sea_turtle.jpg',
    options: [
      { key: 'a', name: 'Turtle' }, // ✅
      { key: 'b', name: 'Crab' },
      { key: 'c', name: 'Stingray' },
    ],
    answer: 'a',
    correct: 'Correct! A Turtle swims across oceans.',
    incorrect: 'It’s a Turtle.',
  },
  {
    key: 'pic-octopus',
    type: 'pic',
    text: 'Which animal is this?',
    image: '/quiz/pics/octopus.jpg',
    options: [
      { key: 'a', name: 'Octopus' }, // ✅
      { key: 'b', name: 'Squid' },
      { key: 'c', name: 'Crab' },
    ],
    answer: 'a',
    correct: 'Yes! Octopuses change color.',
    incorrect: 'It’s an Octopus.',
  },
  {
    key: 'pic-dolphin',
    type: 'pic',
    text: 'Who is this?',
    image: '/quiz/pics/dolphin.jpg',
    options: [
      { key: 'a', name: 'Dolphin' }, // ✅
      { key: 'b', name: 'Shark' },
      { key: 'c', name: 'Seal' },
    ],
    answer: 'a',
    correct: 'Correct! Dolphins are playful mammals.',
    incorrect: 'No—it’s a Dolphin.',
  },
  {
    key: 'pic-starfish',
    type: 'pic',
    text: 'What animal is this?',
    image: '/quiz/pics/starfish.jpg',
    options: [
      { key: 'a', name: 'Starfish' }, // ✅
      { key: 'b', name: 'Crab' },
      { key: 'c', name: 'Jellyfish' },
    ],
    answer: 'a',
    correct: 'Yes! Starfish can regrow arms.',
    incorrect: 'It’s a Starfish.',
  },
];

export default { mcq, tf, match, pic };
