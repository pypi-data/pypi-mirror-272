def spark():
	print('''
scala> val numbersDF = Seq(
 | (1, "Alex", 50.0),
 | (2, "Bob", 20.0),
 | (3, "Cara", 30.0),
 | (4, "Devin", 45.0),
 | (5, "Euro", 75.0)
 | ).toDF("Sr", "Name", "Marks")
numbersDF: org.apache.spark.sql.DataFrame = [Sr: int, Name: string ... 1 
more field]
scala> println("Original DataFrame:")
Original DataFrame:
scala> numbersDF.show()
+---+-----+-----+
| Sr| Name|Marks|
+---+-----+-----+
| 1| Alex| 50.0|
| 2| Bob| 20.0|
| 3| Cara| 30.0|
| 4|Devin| 45.0|
| 5| Euro| 75.0|
+---+-----+-----+
scala> val filteredDF = numbersDF.filter($"Marks" > 20)
filteredDF: org.apache.spark.sql.Dataset[org.apache.spark.sql.Row] = [Sr: 
int, Name: string ... 1 more field]
scala> println("Filtered DataFrame:")
Filtered DataFrame:
scala> filteredDF.show()
+---+-----+-----+
| Sr| Name|Marks|
+---+-----+-----+
| 1| Alex| 50.0|
| 3| Cara| 30.0|
| 4|Devin| 45.0|
| 5| Euro| 75.0|
+---+-----+-----+
scala> val sumDF = 
numbersDF.groupBy("Name").agg(sum("Marks").alias("total_number"), 
sum("Sr").alias("total_value"))
sumDF: org.apache.spark.sql.DataFrame = [Name: string, total_number: 
double ... 1 more field]
scala> println("Sum of numbers and values for each letter:")
Sum of numbers and values for each letter:
scala> sumDF.show()
+-----+------------+-----------+
| Name|total_number|total_value|
+-----+------------+-----------+
| Alex| 50.0| 1|
| Bob| 20.0| 2|
| Cara| 30.0| 3|
|Devin| 45.0| 4|
| Euro| 75.0| 5|
+-----+------------+-----------+
scala> val avgValue = numbersDF.agg(avg("Marks")).first().getDouble(0)
avgValue: Double = 44.0
scala> println("Average value: " + avgValue)
Average value: 44.0
scala> val stdDevValue = 
numbersDF.agg(stddev("Marks")).first().getDouble(0)
stdDevValue: Double = 21.03568396796263
scala> println("Standard deviation of value: " + stdDevValue)
Standard deviation of value: 21.03568396796263
scala> val sortedDF = numbersDF.sort($"Sr".desc)
sortedDF: org.apache.spark.sql.Dataset[org.apache.spark.sql.Row] = [Sr: 
int, Name: string ... 1 more field]
scala> println("Sorted DataFrame:")
Sorted DataFrame:
scala> sortedDF.show()
+---+-----+-----+
| Sr| Name|Marks|
+---+-----+-----+
| 5| Euro| 75.0|
| 4|Devin| 45.0|
| 3| Cara| 30.0|
| 2| Bob| 20.0|
| 1| Alex| 50.0|
+---+-----+-----+
scala> val minValue = numbersDF.agg(min("Marks")).first().getDouble(0)
minValue: Double = 20.0
scala> println("Minimum value: " + minValue)
Minimum value: 20.0
scala> val maxValue = numbersDF.agg(max("Marks")).first().getDouble(0)
maxValue: Double = 75.0
scala> println("Maximum value: " + maxValue)
Maximum value: 75.0''')

spark()