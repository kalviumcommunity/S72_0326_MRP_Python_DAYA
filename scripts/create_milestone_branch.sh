#!/bin/bash
# Quick script to create milestone branches

MILESTONE=$1
BRANCH_NAME=$2
COMMIT_MSG=$3

if [ -z "$MILESTONE" ] || [ -z "$BRANCH_NAME" ] || [ -z "$COMMIT_MSG" ]; then
    echo "Usage: ./create_milestone_branch.sh <milestone_num> <branch_name> <commit_message>"
    echo "Example: ./create_milestone_branch.sh 4 analysis/data-understanding 'Explore datasets'"
    exit 1
fi

echo "Creating branch for Milestone $MILESTONE..."
git checkout main
git pull origin main
git checkout -b $BRANCH_NAME
echo "Branch $BRANCH_NAME created!"
echo ""
echo "After making changes, run:"
echo "  git add ."
echo "  git commit -m \"feat(M$MILESTONE): $COMMIT_MSG\""
echo "  git push -u origin $BRANCH_NAME"
