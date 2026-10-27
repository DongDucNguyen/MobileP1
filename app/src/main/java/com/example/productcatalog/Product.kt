package com.example.productcatalog

data class Product(
    val code: String,
    val name: String,
    val price: Long,
    val category: String,
    val image: String,
    val description: String
)
