export interface Resource {
  title: string;
  category: "books" | "organisations" | "crisis" | "research" | "healing";
  author?: string;
  url?: string;
  phone?: string;
  description: string;
  tags: string[];
  year?: number;
}

export const categoryLabels: Record<string, string> = {
  books: "Books",
  organisations: "Organisations & Support",
  crisis: "Crisis Support",
  research: "Research & Evidence",
  healing: "Healing & Growth",
};

export const resources: Resource[] = [
  // ─── CRISIS SUPPORT ───────────────────────────────────────────────
  {
    title: "Samaritans (UK)",
    category: "crisis",
    url: "https://samaritans.org",
    phone: "116 123",
    description: "Available 24/7 for emotional support. Free to call from any phone.",
    tags: ["uk", "helpline"],
  },
  {
    title: "Mind (UK)",
    category: "crisis",
    url: "https://mind.org.uk",
    description:
      "Mental health support and resources for adults. Information, advice, and local services.",
    tags: ["uk", "mental-health"],
  },
  {
    title: "Crisis Text Line (US)",
    category: "crisis",
    url: "https://crisistextline.org",
    phone: "Text HOME to 741741",
    description:
      "Free 24/7 crisis support via text message. Trained crisis counsellors available any time.",
    tags: ["us", "helpline"],
  },
  {
    title: "988 Suicide & Crisis Lifeline (US)",
    category: "crisis",
    phone: "988",
    url: "https://988lifeline.org",
    description:
      "Call or text 988 for free, confidential support 24/7. Available across the United States.",
    tags: ["us", "helpline"],
  },

  // ─── BOOKS — PARENTAL ALIENATION ──────────────────────────────────
  {
    title: "Divorce Poison: How to Protect Your Family from Bad-Mouthing and Brainwashing",
    category: "books",
    author: "Richard A. Warshak",
    year: 2010,
    description:
      "A cornerstone in modern understanding of parental alienation. Explains how children can be influenced to reject a loving parent and why professionals often misunderstand these cases.",
    tags: ["understanding", "practical"],
  },
  {
    title: "Adult Children of Parental Alienation Syndrome: Breaking the Ties That Bind",
    category: "books",
    author: "Amy J. L. Baker",
    year: 2007,
    description:
      "In-depth interviews with adults who were alienated from a parent during childhood. Explores long-term effects including guilt, identity confusion, and delayed insight.",
    tags: ["understanding", "children"],
  },
  {
    title: "Parental Alienation — Understanding Children Who Reject a Parent",
    category: "books",
    author: "Amy J. L. Baker",
    description:
      "The foundational research-based book on parental alienation from the child's perspective.",
    tags: ["understanding", "children"],
  },
  {
    title: "Surviving Parental Alienation: A Journey of Hope and Healing",
    category: "books",
    author: "Amy J. L. Baker & Paul R. Fine",
    year: 2014,
    description:
      "Centres the voices of targeted parents. Shows how alienation unfolds, how parents experience rejection, and how some relationships are eventually repaired.",
    tags: ["understanding", "practical"],
  },
  {
    title: "Co-parenting with a Toxic Ex",
    category: "books",
    author: "Amy J. L. Baker & Paul Fine",
    description:
      "Practical strategies for managing a high-conflict co-parent. Concrete advice for day-to-day situations.",
    tags: ["practical"],
  },
  {
    title: "Understanding Parental Alienation: Learning to Cope, Helping to Heal",
    category: "books",
    author: "Karen Woodall & Nick Woodall",
    year: 2017,
    description:
      "Approaches alienation through attachment theory and family systems. Explores psychological splitting, alignment as coping strategy, and therapeutic pathways for restoration.",
    tags: ["understanding", "children"],
  },
  {
    title: "Understanding and Managing Parental Alienation: A Guide to Assessment and Intervention",
    category: "books",
    author: "Janet Haines, Mandy Matthewson & Marcus Turnbull",
    year: 2019,
    description:
      "Written for mental health and legal professionals. Provides a structured framework for identifying alienation and distinguishing it from justified estrangement.",
    tags: ["understanding", "legal", "academic"],
  },
  {
    title: "Parental Alienation: An Evidence-Based Approach",
    category: "books",
    author: "Denise McCartan",
    year: 2020,
    description:
      "Concise, methodical application of evidence-based psychological principles. Discusses mild, moderate, and severe alienation, including hybrid cases.",
    tags: ["understanding", "academic"],
  },
  {
    title: "An Attachment-Based Model of Parental Alienation",
    category: "books",
    author: "Craig Childress",
    year: 2015,
    description:
      "Frames parental alienation through attachment system pathology. Provides a detailed framework for assessment using established psychological constructs.",
    tags: ["understanding", "academic"],
  },
  {
    title:
      "Children Held Hostage: Identifying Brainwashed Children, Presenting a Case, and Crafting Solutions",
    category: "books",
    author: "Stanley S. Clawar & Brynne V. Rivlin",
    year: 2013,
    description:
      "Based on study of 1,000+ cases over decades. Examines methods of programming children to reject a parent. A landmark legal resource on presenting evidence in court.",
    tags: ["understanding", "legal", "children"],
  },
  {
    title: "Abandoned Parents: The Devil's Dilemma",
    category: "books",
    author: "Sharon A. Wildey",
    year: 2012,
    description:
      'Addresses the experience of rejected or cut-off parents. Explores the emotional devastation of abandonment and introduces the concept of "silent parenting."',
    tags: ["understanding", "practical"],
  },
  {
    title: "Fault Lines: Fractured Families and How to Mend Them",
    category: "books",
    author: "Karl Pillemer",
    year: 2020,
    description:
      "Based on a national survey of 1,340 Americans. Found 27% of adults estranged from at least one family member. Identifies key triggers and processes of breakdown and repair.",
    tags: ["understanding"],
  },
  {
    title: "The Parental Alienation Syndrome: A Family Therapy and Collaborative Systems Approach",
    category: "books",
    author: "Linda J. Gottlieb",
    year: 2012,
    description:
      "Presents a therapeutic model focusing on restructuring family dynamics and gradually restoring the child's relationship with the targeted parent.",
    tags: ["understanding", "practical"],
  },
  {
    title: "Divorce Casualties: Protecting Your Children from Parental Alienation",
    category: "books",
    author: "Douglas Darnall",
    year: 1998,
    description:
      "Introduces the Three Types of Alienators typology: Naïve, Active, and Obsessed. Practical guide for protecting children during and after divorce.",
    tags: ["understanding", "practical"],
  },
  {
    title: "Children Who Resist Post-Separation Contact With a Parent",
    category: "books",
    author: "Barbara Jo Fidler, Nicholas Bala & Michael A. Saini",
    year: 2013,
    description:
      "Explains how child resistance stems from subtle emotional dynamics invisible to professionals. Shows why alienation cases are difficult because surface behaviour mimics other conditions.",
    tags: ["understanding", "legal", "children", "academic"],
  },
  {
    title:
      "In the Name of the Child: A Developmental Approach to Understanding and Helping Children of Conflicted and Violent Divorce",
    category: "books",
    author: "Janet R. Johnston & Vivienne Roseby",
    year: 1997,
    description:
      "Explains why alienation is invisible to outsiders. Provides a developmental framework for understanding children in high-conflict divorce and the hidden dynamics shaping their behaviour.",
    tags: ["understanding", "children", "academic"],
  },

  // ─── HEALING & GROWTH ─────────────────────────────────────────────
  {
    title: "Man's Search for Meaning",
    category: "healing",
    author: "Viktor E. Frankl",
    year: 1946,
    description:
      "Written by a Holocaust survivor and psychiatrist. When unable to change a situation, we are challenged to change ourselves. The last human freedom is the freedom to choose our attitude in any circumstance.",
    tags: ["practical"],
  },
  {
    title: "The Body Keeps the Score: Brain, Mind, and Body in the Healing of Trauma",
    category: "healing",
    author: "Bessel van der Kolk",
    year: 2014,
    description:
      "Landmark work explaining trauma as defined by powerlessness — both experienced acutely by targeted parents. Demonstrates how trauma physically reshapes the brain and nervous system.",
    tags: ["practical", "academic"],
  },
  {
    title: "The Power of Now: A Guide to Spiritual Enlightenment",
    category: "healing",
    author: "Eckhart Tolle",
    year: 1997,
    description:
      "Work on present-moment awareness and dissolving ego-driven suffering. Not accessible during acute crisis, but deeply valuable once the survival phase has passed.",
    tags: ["practical"],
  },
  {
    title: "The Hero with a Thousand Faces",
    category: "healing",
    author: "Joseph Campbell",
    year: 1949,
    description:
      "The universal Hero's Journey — departure, ordeal, transformation. Reframes alienation not as a dead end but as a crucible producing genuine transformation.",
    tags: ["practical"],
  },
  {
    title: "Building a Life Worth Living: A Memoir",
    category: "healing",
    author: "Marsha M. Linehan",
    year: 2020,
    description:
      "The creator of Dialectical Behaviour Therapy describes her journey through suicidal despair to learning to live. Developed Radical Acceptance: suffering equals pain multiplied by resistance.",
    tags: ["practical"],
  },
  {
    title: "Opening Up: The Healing Power of Expressing Emotions",
    category: "healing",
    author: "James W. Pennebaker",
    year: 1997,
    description:
      "Extensive documentation of the physiological power of expressive writing. Translating traumatic experiences into language boosts immune function and reduces stress response.",
    tags: ["practical", "academic"],
  },
  {
    title: "Influence: The Psychology of Persuasion",
    category: "healing",
    author: "Robert B. Cialdini",
    year: 2021,
    description:
      "Foundational work on social influence. Shows how authority, social proof, and group norms amplify biased narratives and make alienation harder to resist or recognise externally.",
    tags: ["understanding"],
  },
  {
    title: "Attachment and Loss (Volumes 1–3)",
    category: "healing",
    author: "John Bowlby",
    year: 1969,
    description:
      "Foundational attachment theory. Explains how children respond to conflict and the inability to tolerate divided loyalties — the biological and psychological need for secure attachment.",
    tags: ["understanding", "children", "academic"],
  },

  // ─── ORGANISATIONS & SUPPORT ───────────────────────────────────────
  {
    title: "Parental Alienation Study Group (PASG)",
    category: "organisations",
    url: "https://pasg.info",
    description:
      "The world's leading academic body on parental alienation research. International membership of researchers and professionals.",
    tags: ["academic"],
  },
  {
    title: "PASG Research Database",
    category: "organisations",
    url: "https://pasg.info/research",
    description:
      "Comprehensive peer-reviewed research database on parental alienation. Invaluable for court cases and professional reference.",
    tags: ["academic", "legal"],
  },
  {
    title: "NAAP — National Association of Alienated Parents (UK)",
    category: "organisations",
    url: "https://naap.org.uk",
    description:
      "UK-focused advocacy and support for alienated parents. Campaigns for legal recognition and policy change.",
    tags: ["uk"],
  },
  {
    title: "Families Need Fathers (UK)",
    category: "organisations",
    url: "https://fnf.org.uk",
    description:
      "Legal support and campaigning for shared parenting rights. Despite the name, supports all parents — mothers and fathers.",
    tags: ["uk", "legal"],
  },
  {
    title: "Association of Family and Conciliation Courts (AFCC)",
    category: "organisations",
    url: "https://www.afccnet.org",
    description:
      "International interdisciplinary association of professionals dedicated to family court improvement. Developed the Parent–Child Contact Problems framework.",
    tags: ["legal", "academic"],
  },
  {
    title: "High Conflict Institute",
    category: "organisations",
    url: "https://www.highconflictinstitute.com",
    description:
      "Founded by Bill Eddy, LCSW. Provides training and resources on high-conflict personalities. Developed the BIFF Response method (Brief, Informative, Friendly, Firm).",
    tags: ["practical"],
  },
  {
    title: "Family Justice Council — UK Judicial Guidance",
    category: "organisations",
    url: "https://www.judiciary.uk",
    description:
      "Published formal UK judicial guidance (2024) on responding to a child's unexplained reluctance, resistance, or refusal to spend time with a parent.",
    tags: ["uk", "legal"],
  },

  // ─── RESEARCH & EVIDENCE ───────────────────────────────────────────
  {
    title: "Parental Alienating Behaviors: An Unacknowledged Form of Family Violence",
    category: "research",
    author: "Jennifer J. Harman, Edward Kruk & Denise A. Hines",
    year: 2018,
    description:
      "Comprehensive analysis arguing alienating behaviours constitute family violence. Documents tactics including badmouthing, limiting contact, and covert emotional manipulation.",
    tags: ["understanding", "legal", "academic"],
  },
  {
    title: "Prevalence of Parental Alienation Drawn from a Nationally Representative Sample",
    category: "research",
    author: "Jennifer J. Harman, Sadie Leder-Elder & Edward Kruk",
    year: 2019,
    description:
      "Large-scale prevalence study: approximately 13.4% of US/Canadian parents report being targeted by alienating behaviours — equalling 22+ million parents in the US alone.",
    tags: ["understanding", "academic"],
  },
  {
    title: "Parent–Adult Child Estrangement in the United States",
    category: "research",
    author: "Corinne Reczek, Lindsey Stacey & Mieke Beth Thomeer",
    year: 2022,
    description:
      "Most robust US prevalence data: 26% experienced estrangement from father, 6% from mother. Crucially, 69–81% eventually reunited — an important finding for alienated parents.",
    tags: ["understanding", "academic"],
  },
  {
    title: "The Alienated Child: A Reformulation of Parental Alienation Syndrome",
    category: "research",
    author: "Joan B. Kelly & Janet R. Johnston",
    year: 2001,
    description:
      "Widely cited reformulation shifting from PAS labels toward family-systems understanding. Defines the alienated child as one with disproportionate negative feelings driven by loyalty pressure.",
    tags: ["understanding", "children", "academic"],
  },
  {
    title: "Parental Alienation, DSM-5, and ICD-11 — The Five-Factor Model",
    category: "research",
    author: "William Bernet, Wilfrid von Boch-Galhau, Amy J. L. Baker & Stephen L. Morrison",
    year: 2010,
    description:
      "Five-Factor Model for systematically identifying parental alienation without relying on PAS. Used by evaluators and courts for structured assessment.",
    tags: ["understanding", "legal", "academic"],
  },
  {
    title: "Is It Abuse, Alienation, or Estrangement? A Decision Tree",
    category: "research",
    author: "Leslie Drozd & Nancy Olesen",
    year: 2004,
    description:
      "A decision-tree framework for high-conflict custody cases. Helps evaluators and parents distinguish between abuse, alienation, and estrangement.",
    tags: ["understanding", "legal", "academic"],
  },
  {
    title:
      'The Effects of Stereotypes and Suggestions on Preschoolers\' Reports (The "Sam Stone" Study)',
    category: "research",
    author: "Michelle D. Leichtman & Stephen J. Ceci",
    year: 1995,
    description:
      "72% of young children falsely accused a neutral visitor of damage after leading questions and negative stereotypes. Demonstrates how children's memories can be shaped by suggestion.",
    tags: ["children", "academic"],
  },
  {
    title: "Social Science and Parenting Plans for Young Children: A Consensus Report",
    category: "research",
    author: "Richard A. Warshak",
    year: 2015,
    description:
      'Shows courts and professionals frequently mistake fear-based or guilt-induced rejection as a child\'s "authentic preference." Misreading leads to decisions reinforcing alienation.',
    tags: ["legal", "children", "academic"],
  },
  {
    title: "Parental Alienating Behaviours in Separated/Divorced Parents — UK National Survey",
    category: "research",
    author: "Benjamin Hine",
    year: 2025,
    description:
      "UK national survey of 1,005 separated/divorced parents. Confirmed link between alienating behaviours, child contact refusal, and loyalty conflicts. Behaviours are common but extremely hard to detect.",
    tags: ["uk", "understanding", "academic"],
  },
  {
    title: "Parental Alienation — A Valid Experience? (Nordic Study)",
    category: "research",
    author: "Audun Meland et al.",
    year: 2024,
    description:
      "Nordic survey confirming alienation's construct validity. Establishes dose-response links between alienation and relational abuse. Documents significant mental health impacts on targeted parents.",
    tags: ["understanding", "academic"],
  },
  {
    title: "Parent–Adult Child Contact and Estrangement (German Longitudinal Study)",
    category: "research",
    author: "Oliver Arránz Becker & Karsten Hank",
    year: 2022,
    description:
      "Ten-year longitudinal study of 10,228 German adults. 20% estranged from father, 9% from mother. Estrangement from fathers more persistent over time.",
    tags: ["understanding", "academic"],
  },
  {
    title: "Power and Control in Families Affected by Parental Alienation",
    category: "research",
    author: "Jennifer J. Harman, Carla R. Maniotes & Corrin Grubb",
    year: 2021,
    description:
      "Examines how alienating parents use custody advantages and manipulation to maintain dominance. Maps specific power and control dynamics.",
    tags: ["understanding", "legal", "academic"],
  },
  {
    title: "Child Suggestibility and False Memory Formation",
    category: "research",
    author: "Stephen J. Ceci & Maggie Bruck",
    year: 1995,
    description:
      "Landmark experiments showing how repeated gentle suggestion creates vivid false memories in preschoolers. Over 50% recalled fictional events with sensory and emotional detail.",
    tags: ["children", "academic"],
  },
  {
    title: "UK Judicial Guidance on Child Reluctance, Resistance, or Refusal (2024)",
    category: "research",
    author: "Family Justice Council",
    year: 2024,
    description:
      "Formal UK judicial guidance on responding to a child's unexplained reluctance to spend time with a parent. Includes structured pathways for cases involving domestic abuse allegations.",
    tags: ["uk", "legal", "academic"],
  },
  {
    title: "Opening Up by Writing It Down",
    category: "research",
    author: "James W. Pennebaker & Joshua M. Smyth",
    year: 2016,
    description:
      "Research showing that translating traumatic experiences into language boosts immune function, lowers blood pressure, and reduces stress response. Foundation for journalling as therapy.",
    tags: ["practical", "academic"],
  },
];
