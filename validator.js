/**
 * Server-Side Validation Module for TaskGravity Core Node.js Application
 * Implements strict type checking, sanitization, and business rule enforcement.
 */

function validateTaskPayload(data) {
  const errors = {};

  // 1. Title Validation
  if (!data.title || typeof data.title !== 'string') {
    errors.title = 'Task title is required.';
  } else {
    const trimmed = data.title.trim();
    if (trimmed.length < 3) {
      errors.title = 'Task title must be at least 3 characters long.';
    } else if (trimmed.length > 80) {
      errors.title = 'Task title cannot exceed 80 characters.';
    }
  }

  // 2. Category Validation
  const VALID_CATEGORIES = ['Frontend', 'Backend', 'Database', 'DevOps', 'Testing', 'UI/UX'];
  if (!data.category || !VALID_CATEGORIES.includes(data.category)) {
    errors.category = `Category must be one of: ${VALID_CATEGORIES.join(', ')}.`;
  }

  // 3. Priority Validation
  const VALID_PRIORITIES = ['Low', 'Medium', 'High', 'Urgent'];
  if (!data.priority || !VALID_PRIORITIES.includes(data.priority)) {
    errors.priority = `Priority must be one of: ${VALID_PRIORITIES.join(', ')}.`;
  }

  // 4. Due Date Validation
  if (!data.dueDate) {
    errors.dueDate = 'Target deadline date is required (YYYY-MM-DD).';
  } else {
    const parsedDate = new Date(data.dueDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (isNaN(parsedDate.getTime())) {
      errors.dueDate = 'Invalid date format. Use ISO format YYYY-MM-DD.';
    } else if (parsedDate < today) {
      errors.dueDate = 'Deadline cannot be set to a past date.';
    }
  }

  // 5. Estimated Effort (Hours)
  const hours = Number(data.estimatedHours);
  if (data.estimatedHours === undefined || data.estimatedHours === '' || isNaN(hours)) {
    errors.estimatedHours = 'Estimated effort (hours) is required and must be numeric.';
  } else if (hours <= 0) {
    errors.estimatedHours = 'Estimated effort must be greater than 0 hours.';
  } else if (hours > 100) {
    errors.estimatedHours = 'Estimated effort cannot exceed 100 hours.';
  }

  // 6. Description (Optional, but length bounded)
  if (data.description && typeof data.description === 'string' && data.description.trim().length > 300) {
    errors.description = 'Description cannot exceed 300 characters.';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

module.exports = {
  validateTaskPayload
};
