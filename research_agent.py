from google import genai


async def research_topic(session, client, topic):

    print(f"Researching: {topic}")

    # Step 1: Search
    search_result = await session.call_tool(
        "search_web_tool",
        {"topic": topic}
    )

    search_content = "\n".join(
        item.text
        for item in search_result.content
    )

    print("Search complete")

    # Step 2: Generate article
    article_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Create a detailed article about:

        {topic}

        Based on this research:

        {search_content}
        """
    )

    article = article_response.text

    print("Article generated")

    # Step 3: Save file
    filename = (
        topic.lower()
        .replace(" ", "_")
        + "_report.txt"
    )

    await session.call_tool(
        "write_file_tool",
        {
            "filename": filename,
            "content": article
        }
    )

    print("File saved")

    # Step 4: Read file
    file_result = await session.call_tool(
        "read_file_tool",
        {
            "filename": filename
        }
    )

    file_content = "\n".join(
        item.text
        for item in file_result.content
    )

    print("File read")

    # Step 5: Summarize
    summary_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Summarize this report:

        {file_content}
        """
    )

    summary = summary_response.text

    print("Summary created")

    return {
        "filename": filename,
        "summary": summary
    }