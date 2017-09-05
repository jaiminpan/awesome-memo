PG_FUNCTION_INFO_V1(random_string);

Datum
random_string(PG_FUNCTION_ARGS)
{
	int32 length = PG_GETARG_INT32(0);
	int32 i;
	const char chars[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
	const int chars_len;
	char *result;

	if (length < 0)
		PG_RETURN_NULL();

	if (length == 0)
		PG_RETURN_TEXT_P(cstring_to_text(""));

	result = palloc(length + 1);
	if (result == NULL)
		ereport(ERROR, 
				(errcode(ERRCODE_OUT_OF_MEMORY),
				 errmsg("out of memory")));

  chars_len = sizeof(chars) - 1;
	for (i = 0; i < length; i++)
	{
		result[i] = chars[random() % chars_len];
	}
	result[length] = '\0';

	PG_RETURN_TEXT_P(cstring_to_text(result));
}
