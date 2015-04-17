using System;
using System.Reflection;
using Newtonsoft.Json;

namespace api
{

/**
 * Custom conversion of the Light type to a user-friendly format in the scheme of the device JSON serialization.
 */
public class LightConverter : JsonConverter
{
	public override bool CanConvert(Type objectType)
	{
		return objectType == typeof(Light);
	}

	public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
	{
		Light lt = (Light)value;
		writer.WriteValue(lt.Brightness);
	}

	public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
	{
		Light lt = new Light()
		{
			Brightness = (double)reader.Value
		};

		return lt;
	}
}

/**
 * Custom conversion of the Temperature type to a user-friendly format in the scheme of the device JSON serialization. Also avoids redundant values
 * from properties.
 */
public class TemperatureConverter : JsonConverter
{
	public override bool CanConvert(Type objectType)
	{
		return objectType == typeof(Temperature);
	}
	public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
	{
		Temperature tmp = (Temperature)value;
		writer.WriteValue(tmp.C);
	}

	public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
	{
		Temperature tmp = new Temperature()
		{
			C = (double)reader.Value
		};

		return tmp;
	}
}

}
