
docker run -p 7860:7860\
    --env OPENAI_API_KEY\
    --env SNOWFLAKE_USERNAME\
    --env SNOWFLAKE_PASSWORD\
    --env SNOWFLAKE_ROLE\
    --env SNOWFLAKE_WAREHOUSE\
    --env SNOWFLAKE_ACCOUNT\
    --env LLM_SNOWFLAKE_PASSWORD\
    snowflake_llm