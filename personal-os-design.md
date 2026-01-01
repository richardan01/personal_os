# Personal OS for Product Management

## Overview
A comprehensive personal operating system designed to streamline day-to-day product management activities through intelligent agents and modular skills.

---

## Core Agents

### 1. Strategy Agent
**Purpose**: High-level planning and strategic thinking

**Capabilities**:
- Quarterly OKR planning and tracking
- Competitive analysis synthesis
- Market trend monitoring
- Vision and roadmap alignment
- Strategic decision frameworks (SWOT, Porter's Five Forces)

**Daily Triggers**:
- Morning: Review daily priorities against strategic goals
- Weekly: Strategy health check and adjustments
- Monthly: Strategic review and reporting

---

### 2. Discovery Agent
**Purpose**: User research and requirements gathering

**Capabilities**:
- User interview note synthesis
- Feature request categorization and prioritization
- Customer feedback analysis
- User persona maintenance
- Jobs-to-be-Done framework application

**Daily Triggers**:
- Process incoming customer feedback
- Update feature request database
- Flag high-priority user pain points

---

### 3. Planning Agent
**Purpose**: Backlog and sprint management

**Capabilities**:
- User story creation and refinement
- Backlog prioritization (RICE, MoSCoW, Kano)
- Sprint planning assistance
- Dependency mapping
- Capacity planning

**Daily Triggers**:
- Daily standup prep
- Backlog grooming suggestions
- Sprint health monitoring

---

### 4. Execution Agent
**Purpose**: Project tracking and delivery

**Capabilities**:
- Task and milestone tracking
- Risk identification and mitigation
- Blocker escalation
- Progress reporting
- Team coordination

**Daily Triggers**:
- Morning: Day plan generation
- Afternoon: Progress check-in
- Evening: Daily summary and tomorrow prep

---

### 5. Stakeholder Agent
**Purpose**: Communication and alignment

**Capabilities**:
- Stakeholder mapping and analysis
- Communication plan execution
- Meeting agenda preparation
- Status report generation
- Expectation management

**Daily Triggers**:
- Pre-meeting briefings
- Post-meeting action item capture
- Stakeholder update scheduling

---

### 6. Analytics Agent
**Purpose**: Data-driven decision making

**Capabilities**:
- Metric tracking and visualization
- A/B test analysis
- Success criteria monitoring
- Business impact assessment
- Performance trend identification

**Daily Triggers**:
- Daily metrics dashboard update
- Anomaly detection alerts
- Weekly insights summary

---

### 7. Documentation Agent
**Purpose**: Knowledge management

**Capabilities**:
- PRD creation and maintenance
- Decision log tracking
- Wiki/confluence management
- Meeting notes organization
- Process documentation

**Daily Triggers**:
- Auto-save meeting notes
- Document version control
- Knowledge base updates

---

### 8. Learning Agent
**Purpose**: Continuous improvement and growth

**Capabilities**:
- Industry trend curation
- Best practice recommendations
- Skill gap identification
- Learning resource suggestions
- Retrospective facilitation

**Daily Triggers**:
- Morning: Curated reading list
- Weekly: Learning digest
- Bi-weekly: Retrospective preparation

---

## Core Skills Library

### Skill Category: Planning & Prioritization

#### Skill: RICE Prioritization
```
Input: List of features/initiatives
Process: Calculate Reach, Impact, Confidence, Effort scores
Output: Prioritized ranked list
```

#### Skill: OKR Creation
```
Input: Strategic goals
Process: Generate Objectives and Key Results
Output: Structured OKR document with metrics
```

#### Skill: Roadmap Builder
```
Input: Prioritized backlog, team capacity
Process: Timeline allocation with dependencies
Output: Visual roadmap (Now/Next/Later or quarterly)
```

---

### Skill Category: Research & Discovery

#### Skill: User Story Generator
```
Input: Feature request or requirement
Process: Convert to "As a [user], I want [goal], so that [benefit]"
Output: Well-formed user stories with acceptance criteria
```

#### Skill: Interview Synthesizer
```
Input: Raw interview notes
Process: Extract themes, pain points, quotes
Output: Structured insights with actionable recommendations
```

#### Skill: Persona Builder
```
Input: User research data
Process: Identify patterns and segments
Output: Detailed user persona documents
```

---

### Skill Category: Communication

#### Skill: PRD Template Generator
```
Input: Feature requirements
Process: Structure into standard PRD format
Output: Complete PRD with all sections
Sections: Problem, Solution, Users, Success Metrics, Dependencies, Risks
```

#### Skill: Stakeholder Update Creator
```
Input: Project status data
Process: Format for different stakeholder levels
Output: Executive summary, detailed reports, team updates
```

#### Skill: Meeting Agenda Builder
```
Input: Meeting type and participants
Process: Generate relevant agenda items
Output: Structured agenda with time allocations
```

---

### Skill Category: Analytics & Metrics

#### Skill: Metric Dashboard
```
Input: Key metrics to track
Process: Aggregate and visualize data
Output: Real-time dashboard with trends
```

#### Skill: Success Criteria Definer
```
Input: Feature or initiative
Process: Identify measurable success indicators
Output: SMART metrics framework
```

#### Skill: A/B Test Analyzer
```
Input: Test results data
Process: Statistical significance calculation
Output: Recommendation with confidence level
```

---

### Skill Category: Execution

#### Skill: Sprint Planner
```
Input: Backlog items, team velocity
Process: Capacity matching and commitment
Output: Sprint plan with realistic commitments
```

#### Skill: Risk Assessor
```
Input: Project details
Process: Identify potential risks and mitigation
Output: Risk register with severity and probability
```

#### Skill: Dependency Mapper
```
Input: Feature list
Process: Identify cross-team and technical dependencies
Output: Dependency graph with critical path
```

---

### Skill Category: Decision Making

#### Skill: Decision Framework
```
Input: Decision to be made
Process: Apply appropriate framework (DACI, RACI, etc.)
Output: Structured decision document
```

#### Skill: Trade-off Analyzer
```
Input: Competing options
Process: Multi-criteria comparison
Output: Recommendation matrix
```

---

## Daily Workflows

### Morning Routine (8:00 AM - 9:00 AM)
1. **Execution Agent**: Generate today's prioritized task list
2. **Analytics Agent**: Review key metrics dashboard
3. **Stakeholder Agent**: Prepare for scheduled meetings
4. **Learning Agent**: Serve curated reading (5-10 min)

### Mid-Day Check-in (12:00 PM - 12:15 PM)
1. **Execution Agent**: Progress review
2. **Planning Agent**: Adjust priorities if needed
3. **Discovery Agent**: Review new feedback

### Afternoon Focus (2:00 PM - 5:00 PM)
1. **Deep work** on strategic initiatives
2. **Stakeholder Agent**: Facilitate meetings
3. **Documentation Agent**: Capture decisions and notes

### Evening Wrap-up (5:30 PM - 6:00 PM)
1. **Execution Agent**: Daily summary generation
2. **Documentation Agent**: File and organize notes
3. **Planning Agent**: Prep tomorrow's plan
4. **Stakeholder Agent**: Send necessary updates

---

## Weekly Rhythms

### Monday
- **Strategy Agent**: Week kickoff, align on priorities
- **Planning Agent**: Sprint planning (if applicable)
- **Stakeholder Agent**: Send weekly preview

### Wednesday
- **Discovery Agent**: User research sync
- **Analytics Agent**: Mid-week metrics review

### Friday
- **Learning Agent**: Weekly retrospective
- **Documentation Agent**: Knowledge base cleanup
- **Stakeholder Agent**: Weekly summary dispatch

---

## Integration Points

### Tools to Connect
- **Calendar**: Google Calendar, Outlook
- **Task Management**: Jira, Asana, Linear, Notion
- **Communication**: Slack, Teams, Email
- **Analytics**: Mixpanel, Amplitude, Google Analytics
- **Documentation**: Confluence, Notion, Google Docs
- **Design**: Figma, Miro

### Data Flows
```
Feedback Sources → Discovery Agent → Planning Agent → Backlog
Backlog → Planning Agent → Execution Agent → Progress Tracking
Progress → Analytics Agent → Metrics Dashboard → Stakeholder Agent → Updates
All Agents → Documentation Agent → Knowledge Base
```

---

## Customization Guidelines

### For Different Product Roles

#### Product Manager (B2C)
- Emphasize: Analytics Agent, Discovery Agent
- Key Skills: A/B Testing, User Research, Metrics

#### Product Manager (B2B)
- Emphasize: Stakeholder Agent, Strategy Agent
- Key Skills: Customer Success Analysis, Enterprise Roadmapping

#### Technical Product Manager
- Emphasize: Execution Agent, Documentation Agent
- Key Skills: Technical Spec Writing, Dependency Mapping

#### Senior/Lead PM
- Emphasize: Strategy Agent, Stakeholder Agent
- Key Skills: OKR Planning, Cross-functional Leadership

---

## Success Metrics for Personal OS

### Efficiency Metrics
- Time saved on routine tasks (target: 30% reduction)
- Meeting prep time (target: < 15 min per meeting)
- Documentation lag (target: same-day capture)

### Quality Metrics
- Decision quality (retrospective assessment)
- Stakeholder satisfaction scores
- On-time delivery rate

### Growth Metrics
- Learning hours per week
- New skills acquired per quarter
- Cross-functional collaboration score

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- Set up Execution Agent
- Implement basic Planning skills
- Establish daily routines

### Phase 2: Intelligence (Week 3-4)
- Activate Analytics Agent
- Deploy Discovery Agent
- Connect key data sources

### Phase 3: Optimization (Week 5-8)
- Fine-tune all agents
- Custom skill development
- Automation workflows

### Phase 4: Mastery (Ongoing)
- Continuous improvement
- Agent learning and adaptation
- Ecosystem expansion

---

## Notes
- Start simple, add complexity gradually
- Review and adjust weekly
- Maintain human judgment as final decision maker
- Agents augment, not replace, your expertise
