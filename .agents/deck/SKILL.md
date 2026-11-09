---
name: deck
description: Universal presentation creation and editing workflow. Covers speaker-side slide authoring, content structuring, visual communication, and listener-facing presentation development across any format.
---

# Universal Presentation Workflow

A format-independent framework for creating clear, intuitive, and effective presentations.

## 1. Core Principles

### Content First

- Treat each slide as an independent, meaningful unit of communication.
- Prioritise the message being communicated over visual decoration.
- Every slide should have a clear purpose and contribute to the overall narrative.
- Structure content around the audience's understanding and the presenter's delivery requirements.
- Maintain technical accuracy and sufficient supporting context.

### Speaker-Side vs Listener-Facing Distinction

Maintain a strict distinction between two separate presentation layers.

**Speaker-side slides (`.md`)**

- The presenter's working material and source of truth.
- Can contain detailed explanations, paragraphs, technical information, formulas, references, and talking points.
- Prioritise completeness, accuracy, logical flow, and ease of preparation.
- Do not impose large-text or minimal-content restrictions.
- Include sufficient context for the presenter to understand and explain the subject independently.

**Listener-facing slides**

- The actual material displayed to the audience.
- Prioritise immediate comprehension and visual communication.
- Use large, concise text and meaningful visual elements.
- Avoid walls of text and unnecessary technical explanations.
- Retain the information necessary to communicate each slide's message.
- Supporting details should generally be communicated verbally rather than crowded onto the slide.

These two layers serve different purposes and must not be treated as interchangeable. 

> NOTE: Always finish the speaker-side md first and iterate there, only once they are confirmed and done, work on listener side.

### Intuitive Communication

- Make relationships between concepts immediately understandable.
- Prefer diagrams, visual relationships, comparisons, examples, and structured information where appropriate.
- Use concise wording without sacrificing important technical detail.
- Avoid reducing content so aggressively that slides become vague or meaningless.

### Flexible Presentation Design

- Suggest appropriate ways to translate speaker-side content into listener-facing slides.
- Do not enforce a particular presentation format or rendering technology.
- Do not enforce fixed layouts, component libraries, colour palettes, or typography.
- Choose the presentation structure based on the subject and its communication requirements.
- Use space purposefully to improve readability and visual hierarchy.
- Avoid both overcrowded slides and slides with excessive unused space.
- Maintain appropriate text sizes and visual proportions.

## 2. Speaker-Side Slide Authoring

Use individual Markdown (`.md`) files as the primary representation of speaker-side slides.

These files are the source of truth for presentation content. They support the presenter's understanding and delivery rather than directly representing what the audience sees.

Each file represents one slide and should contain the appropriate information needed by the presenter.

Depending on the subject, this may include:

- Slide title and topic.
- Main concepts and detailed explanations.
- Supporting data, formulas, and calculations.
- References and source material.
- Relevant figures or diagram descriptions.
- Oral talking points and explanations.
- Important context that may not appear on the listener-facing slide.

Do not artificially shorten speaker-side content to imitate presentation slides.

### Suggested Organisation

```text
presentation/
├── 01_introduction.md
├── 02_problem.md
├── 03_methodology.md
├── 04_results.md
└── 05_conclusion.md
```

Do not force every slide to follow an identical structure. Select the organisation that best communicates its content and supports the speaker.

## 3. Content Structuring

Before authoring slides:

1. Understand the presentation objective and intended audience.
2. Identify the required topics and information.
3. Establish a logical sequence of ideas.
4. Divide the material into individual slides.
5. Ensure each slide contributes meaningfully to the overall narrative.

When writing individual slides:

- Use headings to establish hierarchy.
- Break complex explanations into understandable sections.
- Use lists only when they improve comprehension.
- Use tables for genuine comparisons or structured data.
- Use diagrams for processes, architectures, relationships, and workflows.
- Use charts when numerical relationships or trends matter.
- Define technical terms and variables when necessary.
- Include references and evidence where appropriate.

The speaker-side slides should retain sufficient information for accurate presentation delivery. Do not prematurely compress them into audience-facing bullet points.

## 4. Visual Communication

The purpose of visual design is to improve understanding. Apply visual principles according to the intended presentation layer.

### Speaker-Side Markdown

- Prioritise structured information and readability.
- Use headings, subsections, lists, tables, and diagrams as appropriate.
- Allow sufficient detail for technical understanding.
- Organise explanations in a logical sequence.
- Avoid unnecessary formatting that makes the material harder to maintain.

### Listener-Facing Slides

- Prioritise large, readable text.
- Avoid dense paragraphs and excessive information.
- Use diagrams, visual relationships, comparisons, and charts where appropriate.
- Maintain meaningful visual balance.
- Avoid arbitrary decorative elements.
- Avoid excessive whitespace that disconnects related information.
- Avoid both overcrowding and excessive unused space.
- Ensure the main message can be understood quickly.

A listener-facing slide should communicate its central message without requiring the audience to read every word.

## 5. Listener-Facing Slide Development

Only begin creating listener-facing presentation slides after the speaker-side Markdown slides have been completed and confirmed.

The listener-facing slides are a separate presentation layer derived from the approved speaker-side content.

For each approved speaker-side slide:

1. Identify its central message.
2. Determine what the audience actually needs to understand.
3. Select an appropriate visual representation.
4. Extract the essential information.
5. Convert detailed explanations into concise presentation content.
6. Preserve technical accuracy and the original narrative.

Do not simply copy Markdown content onto listener-facing slides or compress it mechanically.

The speaker-side material provides the knowledge; the listener-facing material communicates that knowledge.

Presentation format and implementation are flexible. Suggest an appropriate approach based on the task and available tools.

## 6. Iteration and Quality Control

Review the presentation as a complete sequence, not just as individual slides.

### Speaker-Side Review

- Does each slide have a clear purpose?
- Is the narrative logical?
- Are important concepts explained sufficiently?
- Are technical explanations accurate?
- Are formulas, calculations, and variables properly defined?
- Are references and supporting evidence included?
- Does the presenter have sufficient context to explain the material?

### Listener-Facing Review

- Is the central message immediately understandable?
- Is the text sufficiently large and readable?
- Are diagrams and figures meaningful?
- Is the visual hierarchy effective?
- Is any content unnecessarily repetitive?
- Is there excessive unused space?
- Are slides overcrowded?
- Does each slide accurately represent the approved speaker-side content?

When editing, preserve correct existing content and structure unless there is a clear reason to change them.

Prioritise meaningful improvements over cosmetic changes.

## 7. General Rule

The presentation should communicate the intended information as clearly and efficiently as possible.

Content determines structure. Structure determines presentation. Presentation format is an implementation choice, not a constraint.

**Speaker-side Markdown first. Listener-facing presentation second.**

Never confuse the presenter's working material with the audience's presentation material.