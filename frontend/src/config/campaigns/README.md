# Campaign Configuration System

## 📋 Overview

Campaign configuration system for triggers and actions. 

**CURRENT STATUS**: All campaigns (Attraction, Nurturing, Recruitment) currently share the same 12 triggers and 9 actions. Campaign-specific filtering will be implemented when requirements are documented.

## 🏗️ Structure

```
config/campaigns/
├── index.js              # Central export & helper functions
├── commonConfig.js       # Shared config for all campaigns (ACTIVE)
├── attractionConfig.js   # Attraction-specific config (READY for future use)
├── nurturingConfig.js    # Nurturing-specific config (READY for future use)
├── recruitmentConfig.js  # Recruitment-specific config (READY for future use)
└── README.md            # This file
```

## 🎯 Current Configuration

### **ALL Campaigns** (Attraction, Nurturing, Recruitment)
Currently share the same configuration based on documentation:
- **Triggers**: 12 types
  - Talent Interactions: ON_FORM_SUBMISSION, ON_LINK_CLICK, ON_EMAIL_OPEN, ON_JOB_APPLICATION, ON_UNSUBSCRIBE
  - Data Management: ON_TAG_ADDED, ON_TAG_REMOVED
  - System Interactions: ON_STATUS_CHANGED, ON_SCORE_REACHED, ON_EMAIL_BOUNCE, ON_INACTIVITY_TIMEOUT, ON_SEQUENCE_COMPLETED
- **Actions**: 9 types (EMAIL, MESSAGE, UPDATE_FIELD_VALUE, ADD_TAG, REMOVE_TAG, CHANGE_STATUS, STOP_TRACKING, INTERNAL_NOTIFICATION, HANDOFF_TO_ATS)

## 🔮 Future Campaign-Specific Configurations (Ready but not active)

### **ATTRACTION** Campaign (Prepared)
Focus: Marketing & initial outreach to attract talent
- **Triggers**: 17 types (simplified list)
- **Actions**: 12 types (focused on outreach)

### **NURTURING** Campaign (Prepared)
Focus: Engagement sequences and relationship building
- **Triggers**: 20 types (full list)
- **Actions**: 19 types (full list with sequences)

### **RECRUITMENT** Campaign (Prepared)
Focus: Candidate management and hiring process
- **Triggers**: 20 types (full list)
- **Actions**: 19 types (recruitment-focused descriptions)

## 📖 Usage

### In Step3_Settings.vue components:

```javascript
import { 
  CAMPAIGN_TYPES,
  getTriggerTypes, 
  getActionTypes,
  getTriggerIcon as getCampaignTriggerIcon, 
  getTriggerLabel as getCampaignTriggerLabel, 
  getTriggerDescription as getCampaignTriggerDescription,
  getActionIcon as getCampaignActionIcon, 
  getActionLabel as getCampaignActionLabel, 
  getActionDescription as getCampaignActionDescription
} from '../../../config/campaigns'

// Set campaign type
const CAMPAIGN_TYPE = CAMPAIGN_TYPES.ATTRACTION // or NURTURING, RECRUITMENT

// Get campaign-specific options
const triggerTypeOptions = getTriggerTypes(CAMPAIGN_TYPE)
const actionTypeOptions = getActionTypes(CAMPAIGN_TYPE)

// Create wrapper functions
const getTriggerIcon = (triggerType) => getCampaignTriggerIcon(triggerType, CAMPAIGN_TYPE)
const getTriggerLabel = (triggerType) => getCampaignTriggerLabel(triggerType, CAMPAIGN_TYPE)
// ... etc
```

### Direct function calls:

```javascript
// Get trigger types for attraction campaign
const triggers = getTriggerTypes(CAMPAIGN_TYPES.ATTRACTION)

// Get action icon for nurturing campaign
const icon = getActionIcon('EMAIL', CAMPAIGN_TYPES.NURTURING)

// Get trigger description for recruitment campaign
const desc = getTriggerDescription('ON_JOB_APPLICATION', CAMPAIGN_TYPES.RECRUITMENT)
```

## 🔧 Adding New Campaign Type

1. Create new config file: `newCampaignConfig.js`
2. Export trigger/action types, icons, and descriptions
3. Add to `index.js`:
   ```javascript
   import { ... } from './newCampaignConfig'
   
   export const CAMPAIGN_TYPES = {
     ...
     NEW_CAMPAIGN: 'new_campaign'
   }
   
   // Add to helper functions
   ```

## 📝 Adding New Trigger/Action Type

### Option 1: Add to specific campaign only

Edit the specific config file (e.g., `attractionConfig.js`):

```javascript
export const attractionTriggerTypes = [
  // ... existing triggers
  { label: __('New Trigger'), value: 'NEW_TRIGGER' }
]

export const attractionTriggerIcons = {
  // ... existing icons
  'NEW_TRIGGER': 'icon-name'
}

export const attractionTriggerDescriptions = {
  // ... existing descriptions
  'NEW_TRIGGER': __('Description of new trigger')
}
```

### Option 2: Add to all campaigns

Add to all 3 config files if the trigger/action is universal.

## 🎨 Customization Per Campaign

Each campaign can have:
- **Different trigger lists** (e.g., Attraction doesn't need SCHEDULED_TIME)
- **Different action lists** (e.g., Attraction doesn't need SMART_DELAY)
- **Different descriptions** (same trigger, different context)
- **Different icons** (if needed for visual differentiation)

## ✅ Benefits

1. **Maintainability**: Each campaign config is isolated
2. **Flexibility**: Easy to add/remove triggers per campaign
3. **Consistency**: Shared helpers ensure consistent behavior
4. **Scalability**: Easy to add new campaign types
5. **Type Safety**: Central enum for campaign types
6. **Clarity**: Clear separation of concerns

## 🚀 Enabling Campaign-Specific Filtering (When Ready)

When requirements are documented, uncomment the TODO sections in `index.js`:

### Step 1: In `getTriggerTypes()` function:
```javascript
export function getTriggerTypes(campaignType) {
  // Uncomment these lines:
  const config = {
    [CAMPAIGN_TYPES.ATTRACTION]: attractionTriggerTypes,
    [CAMPAIGN_TYPES.NURTURING]: nurturingTriggerTypes,
    [CAMPAIGN_TYPES.RECRUITMENT]: recruitmentTriggerTypes
  }
  return config[campaignType] || allTriggerTypes
  
  // Remove this line:
  // return allTriggerTypes
}
```

### Step 2: Repeat for other functions:
- `getActionTypes()`
- `getTriggerIcon()`
- `getTriggerDescription()`
- `getActionIcon()`
- `getActionDescription()`

### Step 3: Test each campaign:
- Verify Attraction has correct limited set
- Verify Nurturing has full set
- Verify Recruitment has full set with recruitment context

## 📚 Best Practices

1. Always use `CAMPAIGN_TYPES` enum instead of hardcoded strings
2. Create wrapper functions in components to avoid repeating campaign type
3. Keep descriptions contextual to campaign purpose
4. Document any campaign-specific business logic
5. Test each campaign independently after changes

## 🔍 Example Differences

**Attraction**: Simple, focused on initial outreach
- Triggers: ON_CREATE, ON_EMAIL_OPEN, ON_JOB_APPLICATION
- Actions: EMAIL, SMS, ADD_TAG, SEND_NOTIFICATION

**Nurturing**: Complex sequences with smart delays
- Triggers: + ON_SEQUENCE_COMPLETED, ON_SCHEDULED_TIME
- Actions: + SMART_DELAY, AI_CALL, HANDOFF_TO_ATS

**Recruitment**: Focus on candidate tracking
- Triggers: (same as Nurturing)
- Actions: (same as Nurturing but different descriptions)
- Emphasis on CHANGE_STATUS, HANDOFF_TO_ATS
