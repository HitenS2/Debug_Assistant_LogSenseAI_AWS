# Design Document: Restaurant Review Application

## Overview

The restaurant review application is a web-based system that allows users to browse restaurants, view details, submit reviews, and rate establishments. The design emphasizes simplicity with a plain UI that uses minimal styling and standard HTML elements.

The application follows a client-side architecture with local storage for data persistence, making it lightweight and easy to deploy without requiring a backend server.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────┐
│         User Interface Layer        │
│  (HTML + Plain CSS + JavaScript)    │
└─────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│       Application Logic Layer       │
│   (Restaurant & Review Management)  │
└─────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│         Data Storage Layer          │
│        (Browser LocalStorage)       │
└─────────────────────────────────────┘
```

### Technology Stack

- **Frontend**: Vanilla JavaScript (ES6+), HTML5, Plain CSS
- **Storage**: Browser LocalStorage API
- **No external dependencies**: Pure web standards only

## Components and Interfaces

### 1. Data Models

#### Restaurant Model

```javascript
Restaurant {
  id: string              // Unique identifier (UUID)
  name: string           // Restaurant name
  cuisineType: string    // Type of cuisine (e.g., "Italian", "Chinese")
  address: string        // Physical address
  reviews: Review[]      // Array of reviews
  averageRating: number  // Calculated average (0 if no reviews)
}
```

#### Review Model

```javascript
Review {
  id: string           // Unique identifier (UUID)
  restaurantId: string // Reference to parent restaurant
  reviewerName: string // Name of the reviewer
  rating: number       // Integer 1-5
  reviewText: string   // Review content
  date: string         // ISO 8601 timestamp
}
```

### 2. Storage Manager

Handles all interactions with browser LocalStorage.

```javascript
StorageManager {
  // Load all restaurants from storage
  loadRestaurants(): Restaurant[]
  
  // Save all restaurants to storage
  saveRestaurants(restaurants: Restaurant[]): void
  
  // Clear all data (for testing/reset)
  clearAll(): void
}
```

**Implementation Notes:**
- Data stored as JSON string under key "restaurants"
- Reviews embedded within restaurant objects
- Automatic serialization/deserialization

### 3. Restaurant Manager

Core business logic for restaurant operations.

```javascript
RestaurantManager {
  restaurants: Restaurant[]
  
  // Initialize and load data
  constructor()
  
  // Get all restaurants
  getAllRestaurants(): Restaurant[]
  
  // Get restaurant by ID
  getRestaurantById(id: string): Restaurant | null
  
  // Add new restaurant
  addRestaurant(name: string, cuisineType: string, address: string): Restaurant
  
  // Search restaurants by name (case-insensitive)
  searchRestaurants(searchTerm: string): Restaurant[]
  
  // Filter restaurants by cuisine type
  filterByCuisine(cuisineType: string): Restaurant[]
  
  // Get unique cuisine types
  getCuisineTypes(): string[]
  
  // Add review to restaurant
  addReview(restaurantId: string, reviewerName: string, rating: number, reviewText: string): Review
  
  // Calculate average rating for a restaurant
  calculateAverageRating(restaurantId: string): number
  
  // Save current state to storage
  save(): void
}
```

### 4. UI Controller

Manages DOM manipulation and user interactions.

```javascript
UIController {
  restaurantManager: RestaurantManager
  currentView: string  // "list" | "detail" | "add-restaurant"
  currentRestaurantId: string | null
  
  // Initialize UI and event listeners
  init(): void
  
  // Render restaurant list view
  renderRestaurantList(restaurants: Restaurant[]): void
  
  // Render restaurant detail view
  renderRestaurantDetail(restaurantId: string): void
  
  // Render add restaurant form
  renderAddRestaurantForm(): void
  
  // Handle search input
  handleSearch(searchTerm: string): void
  
  // Handle cuisine filter
  handleCuisineFilter(cuisineType: string): void
  
  // Handle add restaurant form submission
  handleAddRestaurant(event: Event): void
  
  // Handle add review form submission
  handleAddReview(event: Event): void
  
  // Show error message
  showError(message: string): void
  
  // Clear error message
  clearError(): void
}
```

### 5. Validation Module

Input validation utilities.

```javascript
Validator {
  // Validate restaurant data
  validateRestaurant(name: string, cuisineType: string, address: string): ValidationResult
  
  // Validate review data
  validateReview(reviewerName: string, rating: number, reviewText: string): ValidationResult
  
  // Check if string is non-empty after trimming
  isNonEmptyString(value: string): boolean
  
  // Check if rating is valid (1-5 integer)
  isValidRating(rating: number): boolean
}

ValidationResult {
  valid: boolean
  errors: string[]
}
```

## Data Models

### Restaurant Storage Format

```json
{
  "restaurants": [
    {
      "id": "uuid-1",
      "name": "Mario's Pizza",
      "cuisineType": "Italian",
      "address": "123 Main St",
      "reviews": [
        {
          "id": "review-uuid-1",
          "restaurantId": "uuid-1",
          "reviewerName": "John Doe",
          "rating": 5,
          "reviewText": "Excellent pizza!",
          "date": "2024-01-15T10:30:00Z"
        }
      ],
      "averageRating": 5.0
    }
  ]
}
```

### Rating Calculation

Average rating is calculated as:
```
averageRating = sum(all ratings) / count(all ratings)
```

Rounded to 1 decimal place for display.
If no reviews exist, averageRating = 0.

## User Interface Design

### Page Structure

The application uses a single-page layout with three main views:

1. **Restaurant List View** (default)
2. **Restaurant Detail View**
3. **Add Restaurant Form View**

### HTML Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>Restaurant Reviews</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>Restaurant Reviews</h1>
    <button id="add-restaurant-btn">Add Restaurant</button>
  </header>
  
  <main>
    <!-- Search and Filter Section -->
    <div id="controls">
      <input type="text" id="search-input" placeholder="Search restaurants...">
      <select id="cuisine-filter">
        <option value="">All Cuisines</option>
      </select>
    </div>
    
    <!-- Error Message Area -->
    <div id="error-message" class="hidden"></div>
    
    <!-- Dynamic Content Area -->
    <div id="content">
      <!-- Restaurant list, detail, or form rendered here -->
    </div>
  </main>
  
  <script src="app.js"></script>
</body>
</html>
```

### CSS Styling (Plain Design)

```css
/* Minimal, plain styling */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ccc;
}

button {
  padding: 8px 16px;
  cursor: pointer;
}

input, select, textarea {
  padding: 8px;
  margin: 5px 0;
  width: 100%;
  max-width: 400px;
}

.restaurant-item {
  padding: 15px;
  margin: 10px 0;
  border: 1px solid #ddd;
}

.hidden {
  display: none;
}

.error {
  color: red;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid red;
}
```

### View Templates

#### Restaurant List Item

```html
<div class="restaurant-item" data-id="{id}">
  <h3>{name}</h3>
  <p>Cuisine: {cuisineType}</p>
  <p>Rating: {averageRating} ★</p>
  <button class="view-details-btn">View Details</button>
</div>
```

#### Restaurant Detail View

```html
<div class="restaurant-detail">
  <button id="back-btn">← Back to List</button>
  <h2>{name}</h2>
  <p>Cuisine: {cuisineType}</p>
  <p>Address: {address}</p>
  <p>Average Rating: {averageRating} ★</p>
  
  <h3>Reviews</h3>
  <div id="reviews-list">
    <!-- Review items rendered here -->
  </div>
  
  <h3>Add Your Review</h3>
  <form id="add-review-form">
    <input type="text" id="reviewer-name" placeholder="Your name" required>
    <select id="rating" required>
      <option value="">Select rating</option>
      <option value="1">1 ★</option>
      <option value="2">2 ★</option>
      <option value="3">3 ★</option>
      <option value="4">4 ★</option>
      <option value="5">5 ★</option>
    </select>
    <textarea id="review-text" placeholder="Write your review" required></textarea>
    <button type="submit">Submit Review</button>
  </form>
</div>
```

#### Review Item

```html
<div class="review-item">
  <p><strong>{reviewerName}</strong> - {rating} ★</p>
  <p>{reviewText}</p>
  <p><small>{date}</small></p>
</div>
```

#### Add Restaurant Form

```html
<div class="add-restaurant-form">
  <button id="back-btn">← Back to List</button>
  <h2>Add New Restaurant</h2>
  <form id="add-restaurant-form">
    <input type="text" id="restaurant-name" placeholder="Restaurant name" required>
    <input type="text" id="cuisine-type" placeholder="Cuisine type" required>
    <input type="text" id="address" placeholder="Address" required>
    <button type="submit">Add Restaurant</button>
  </form>
</div>
```

## Application Flow

### Initialization Flow

```
1. Page loads
2. StorageManager loads data from LocalStorage
3. RestaurantManager initializes with loaded data
4. UIController renders restaurant list view
5. Event listeners attached to controls
```

### Add Restaurant Flow

```
1. User clicks "Add Restaurant" button
2. UIController renders add restaurant form
3. User fills form and submits
4. Validator checks all fields are non-empty
5. If valid: RestaurantManager creates restaurant
6. Restaurant saved to storage
7. UIController returns to list view with new restaurant
8. If invalid: Error message displayed
```

### View Restaurant Details Flow

```
1. User clicks "View Details" on restaurant
2. UIController renders detail view with restaurant data
3. All reviews displayed
4. Add review form rendered
```

### Submit Review Flow

```
1. User fills review form and submits
2. Validator checks all fields and rating range
3. If valid: RestaurantManager adds review to restaurant
4. Average rating recalculated
5. Data saved to storage
6. UIController re-renders detail view with new review
7. If invalid: Error message displayed
```

### Search Flow

```
1. User types in search input
2. UIController calls RestaurantManager.searchRestaurants()
3. Filtered results rendered
4. If no results: "No restaurants found" message displayed
```

### Filter Flow

```
1. User selects cuisine from dropdown
2. UIController calls RestaurantManager.filterByCuisine()
3. Filtered results rendered
4. If no results: "No restaurants found" message displayed
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified the following redundancies:
- **3.6 and 4.4** both test that average ratings update after adding reviews - these can be combined into a single comprehensive property
- **Rating validation (3.5 and 4.1)** both test valid rating ranges - these can be combined
- **Field validation for reviews (3.2, 3.4) and restaurants (6.2, 6.4)** follow the same pattern - we'll create properties that cover the validation comprehensively

### Properties

**Property 1: Restaurant list display completeness**
*For any* restaurant, when rendered in the list view, the output should contain the restaurant's name, cuisine type, and average rating.
**Validates: Requirements 1.1**

**Property 2: Average rating calculation correctness**
*For any* restaurant with reviews, the displayed average rating should equal the mean of all review ratings for that restaurant, rounded to one decimal place.
**Validates: Requirements 1.3, 4.2, 4.3**

**Property 3: Restaurant detail display completeness**
*For any* restaurant, when rendered in the detail view, the output should contain the restaurant's name, cuisine type, address, and average rating.
**Validates: Requirements 2.1**

**Property 4: All reviews displayed**
*For any* restaurant, when rendered in the detail view, all reviews in the restaurant's Review_List should appear in the output.
**Validates: Requirements 2.2**

**Property 5: Review display completeness**
*For any* review, when rendered, the output should contain the reviewer name, rating, review text, and submission date.
**Validates: Requirements 2.3**

**Property 6: Valid review acceptance**
*For any* review with non-empty reviewer name, rating between 1-5 inclusive, and non-empty review text, the system should accept the review and add it to the restaurant's Review_List.
**Validates: Requirements 3.2, 3.3, 4.1**

**Property 7: Invalid review rejection**
*For any* review with missing required fields (empty reviewer name, missing rating, or empty review text), the system should reject the submission and display an error message.
**Validates: Requirements 3.2, 3.4**

**Property 8: Invalid rating rejection**
*For any* rating value outside the range [1, 5], the system should reject the submission.
**Validates: Requirements 3.5, 4.1**

**Property 9: Average rating update after review**
*For any* restaurant, after adding a valid review, the restaurant's average rating should be immediately recalculated to reflect the new review.
**Validates: Requirements 3.6, 4.4**

**Property 10: Search filtering correctness**
*For any* search term and restaurant list, the filtered results should contain only restaurants whose names contain the search term (case-insensitive), and all matching restaurants should be included.
**Validates: Requirements 5.2**

**Property 11: Cuisine filtering correctness**
*For any* cuisine type and restaurant list, the filtered results should contain only restaurants with that exact cuisine type, and all matching restaurants should be included.
**Validates: Requirements 5.4**

**Property 12: Valid restaurant acceptance**
*For any* restaurant with non-empty name, non-empty cuisine type, and non-empty address, the system should accept the restaurant and add it to the Restaurant_List.
**Validates: Requirements 6.2, 6.3**

**Property 13: Invalid restaurant rejection**
*For any* restaurant with missing required fields (empty name, empty cuisine type, or empty address), the system should reject the submission and display an error message.
**Validates: Requirements 6.2, 6.4**

**Property 14: New restaurant initialization**
*For any* newly added restaurant, its average rating should be initialized to 0 and its Review_List should be empty.
**Validates: Requirements 6.5**

**Property 15: Restaurant persistence round-trip**
*For any* restaurant added to the system, saving to storage and then loading from storage should produce an equivalent restaurant with the same data.
**Validates: Requirements 7.1, 7.3**

**Property 16: Review persistence round-trip**
*For any* review added to a restaurant, saving to storage and then loading from storage should produce an equivalent review with the same data.
**Validates: Requirements 7.2, 7.3**

## Error Handling

### Validation Errors

**Invalid Restaurant Data:**
- **Missing name**: Display "Restaurant name is required"
- **Missing cuisine type**: Display "Cuisine type is required"
- **Missing address**: Display "Address is required"
- **Multiple missing fields**: Display all applicable error messages

**Invalid Review Data:**
- **Missing reviewer name**: Display "Reviewer name is required"
- **Missing rating**: Display "Rating is required"
- **Invalid rating value**: Display "Rating must be between 1 and 5"
- **Missing review text**: Display "Review text is required"
- **Multiple missing fields**: Display all applicable error messages

### Storage Errors

**LocalStorage Unavailable:**
- Detect if LocalStorage is not supported
- Display warning: "Data persistence is not available in this browser"
- Continue with in-memory storage only

**Storage Quota Exceeded:**
- Catch QuotaExceededError when saving
- Display error: "Unable to save data - storage limit reached"
- Suggest clearing old data

**Corrupted Data:**
- If JSON parsing fails during load, log error to console
- Initialize with empty restaurant list
- Display warning: "Unable to load previous data - starting fresh"

### User Experience

**Error Display:**
- Show errors in a dedicated error message area
- Use red text and border for visibility
- Clear errors when user corrects input or navigates away
- Errors should be specific and actionable

**Graceful Degradation:**
- If storage fails, app continues to work with in-memory data
- If data is corrupted, app starts fresh rather than crashing
- All errors are caught and handled, never showing raw exceptions to users

## Testing Strategy

### Dual Testing Approach

The application will use both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs using randomized testing

Both approaches are complementary and necessary. Unit tests catch concrete bugs and verify specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing

**Library Selection:**
- Use **fast-check** for JavaScript property-based testing
- Fast-check provides generators for primitive types and complex objects
- Supports custom generators for domain models

**Test Configuration:**
- Each property test runs a minimum of 100 iterations
- Each test references its design document property number
- Tag format: `// Feature: restaurant-review-app, Property N: [property text]`

**Custom Generators:**
- `arbitraryRestaurant()`: Generates random restaurants with valid data
- `arbitraryReview()`: Generates random reviews with valid ratings
- `arbitraryInvalidReview()`: Generates reviews with intentionally invalid data
- `arbitrarySearchTerm()`: Generates random search strings

**Property Test Coverage:**
- All 16 correctness properties will have corresponding property tests
- Each property test validates the universal behavior across randomized inputs
- Tests verify both positive cases (valid inputs accepted) and negative cases (invalid inputs rejected)

### Unit Testing

**Library Selection:**
- Use **Jest** for JavaScript unit testing
- Jest provides good assertion library and mocking capabilities

**Unit Test Focus:**
- Specific examples demonstrating correct behavior
- Edge cases: empty lists, no reviews, boundary ratings (1 and 5)
- Error conditions: missing fields, invalid ratings, storage failures
- Integration points: UI controller interactions with restaurant manager

**Test Organization:**
```
tests/
  ├── unit/
  │   ├── storage-manager.test.js
  │   ├── restaurant-manager.test.js
  │   ├── validator.test.js
  │   └── ui-controller.test.js
  └── property/
      ├── restaurant-properties.test.js
      ├── review-properties.test.js
      ├── search-properties.test.js
      └── persistence-properties.test.js
```

### Test Coverage Goals

- **Unit tests**: Cover all edge cases and error paths
- **Property tests**: Cover all correctness properties (100+ iterations each)
- **Integration tests**: Verify end-to-end flows work correctly
- **Target**: 90%+ code coverage across all modules

### Example Property Test

```javascript
// Feature: restaurant-review-app, Property 2: Average rating calculation correctness
test('average rating equals mean of all review ratings', () => {
  fc.assert(
    fc.property(
      fc.array(fc.integer({ min: 1, max: 5 }), { minLength: 1 }),
      (ratings) => {
        const restaurant = createRestaurantWithRatings(ratings);
        const expectedAverage = ratings.reduce((a, b) => a + b) / ratings.length;
        const roundedExpected = Math.round(expectedAverage * 10) / 10;
        expect(restaurant.averageRating).toBe(roundedExpected);
      }
    ),
    { numRuns: 100 }
  );
});
```

### Example Unit Test

```javascript
test('empty restaurant list shows appropriate message', () => {
  const manager = new RestaurantManager();
  const restaurants = manager.getAllRestaurants();
  expect(restaurants).toHaveLength(0);
  
  const ui = new UIController(manager);
  ui.renderRestaurantList(restaurants);
  
  const content = document.getElementById('content').textContent;
  expect(content).toContain('No restaurants available');
});
```

### Testing Edge Cases

The following edge cases will be explicitly tested with unit tests:
- Empty restaurant list (Requirements 1.2)
- Restaurant with no reviews (Requirements 2.4)
- Empty search results (Requirements 5.5)
- Empty storage on startup (Requirements 7.4)
- Whitespace-only input fields
- Boundary ratings (1 and 5)
- Very long restaurant names and review text
- Special characters in search terms

### Manual Testing Checklist

While automated tests cover functionality, manual testing should verify:
- UI layout is plain and readable
- Forms are easy to use
- Navigation between views works smoothly
- Error messages are clear and helpful
- Data persists across browser sessions
- Application works in different browsers (Chrome, Firefox, Safari)
