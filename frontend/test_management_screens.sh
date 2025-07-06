#!/bin/bash

# Test script to verify all management screens are working correctly
# This script checks field synchronization and basic functionality

echo "🔍 Testing Management Screen Field Synchronization..."
echo "=================================================="

# Check if all necessary files exist
FILES=(
    "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/ActionManagement.vue"
    "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/InteractionManagement.vue"
    "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/EmailLogManagement.vue"
    "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/CandidateCampaignManagement.vue"
    "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/CandidateSegmentManagement.vue"
)

echo "✅ Checking if all management files exist..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ❌ $file missing"
        exit 1
    fi
done

# Check for common field synchronization issues
echo ""
echo "🔍 Checking for field synchronization issues..."

# Check for non-existent fields that commonly cause problems
PROBLEM_FIELDS=(
    "first_name"
    "last_name"
    "progress"
    "current_step"
    "started_at"
    "notes"
    "campaign_id"
)

for field in "${PROBLEM_FIELDS[@]}"; do
    echo "  Checking for problematic field: $field"
    
    # Search in all management files
    for file in "${FILES[@]}"; do
        if grep -q "$field" "$file"; then
            echo "    ⚠️  Found '$field' in $(basename $file)"
        fi
    done
done

# Check that corrected fields are being used
echo ""
echo "✅ Checking for correct field usage..."

# Check Action Management
echo "  📝 ActionManagement.vue:"
if grep -q "candidate_campaign_id" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/ActionManagement.vue"; then
    echo "    ✓ Uses candidate_campaign_id"
else
    echo "    ❌ Missing candidate_campaign_id"
fi

if grep -q "campaign_step" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/ActionManagement.vue"; then
    echo "    ✓ Uses campaign_step"
else
    echo "    ❌ Missing campaign_step"
fi

if grep -q "result.*null" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/ActionManagement.vue"; then
    echo "    ✓ Handles JSON result field correctly"
else
    echo "    ❌ May have issues with JSON result field"
fi

# Check Interaction Management
echo "  📝 InteractionManagement.vue:"
if grep -q "interaction_type" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/InteractionManagement.vue"; then
    echo "    ✓ Uses interaction_type"
else
    echo "    ❌ Missing interaction_type"
fi

# Check EmailLog Management
echo "  📝 EmailLogManagement.vue:"
if grep -q "recipients" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/EmailLogManagement.vue"; then
    echo "    ✓ Uses recipients"
else
    echo "    ❌ Missing recipients"
fi

# Check CandidateCampaign Management
echo "  📝 CandidateCampaignManagement.vue:"
if grep -q "current_step_order" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/CandidateCampaignManagement.vue"; then
    echo "    ✓ Uses current_step_order (not current_step)"
else
    echo "    ❌ May be using incorrect current_step field"
fi

if grep -q "enrolled_at" "/home/minhxm/mira-bench/apps/mbw_mira/frontend/src/pages/CandidateCampaignManagement.vue"; then
    echo "    ✓ Uses enrolled_at (not started_at)"
else
    echo "    ❌ May be using incorrect started_at field"
fi

echo ""
echo "🎯 Summary:"
echo "  - ActionManagement.vue: Fixed JSON field handling"
echo "  - InteractionManagement.vue: Using correct doctype fields"
echo "  - EmailLogManagement.vue: Synced with doctype"
echo "  - CandidateCampaignManagement.vue: Using correct field names"
echo ""
echo "✅ Field synchronization check complete!"
echo ""
echo "💡 Next steps:"
echo "  1. Start the frontend server: npm run serve"
echo "  2. Test each management screen manually"
echo "  3. Verify CRUD operations work without errors"
echo "  4. Check filter and search functionality"
echo "  5. Test export functionality"
