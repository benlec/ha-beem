# Historical Data Fetching in Beem Integration

## Configuration

Historical data fetching can now be enabled during the integration setup:

1. When adding the Beem Energy integration, you'll see a "Number of months of historical data to fetch" option
2. Enter a number between 0 and 12 to specify how many months of historical data you want to retrieve
3. The setting can be configured separately for each Beem Energy account:
   - Setting 0 (default) will only fetch current month data
   - Setting 1-12 will fetch that many months of historical data
   - For example, setting 3 will fetch data for the current month plus the previous 2 months

This feature helps provide a more complete picture of your solar energy production by including historical data in your Home Assistant instance.

## Current State
The Beem integration currently fetches data for the current month only, using the `get_box_summary()` API method. This method accepts month and year parameters, which means we can fetch historical data from any month.

## Implementation Possibilities

We can implement historical data fetching in two ways:

1. **Manual Import**: Add a service that allows users to specify a date range and fetch historical data for that period.
2. **Automatic Backfill**: When the integration is first set up, automatically fetch data for the past X months.

## Proposed Changes

The recommended approach is to implement a service called `fetch_historical_data` that allows users to fetch historical data for a specified period. This provides more flexibility and control to the users.

Key changes needed:
1. Add a new service to fetch historical data
2. Store the historical data in Home Assistant's recorder
3. Update the coordinator to handle historical data fetching

## Implementation Steps
The code changes will:
1. Add a new service definition
2. Extend the coordinator to support historical data fetching
3. Add state class configuration to ensure proper long-term statistics