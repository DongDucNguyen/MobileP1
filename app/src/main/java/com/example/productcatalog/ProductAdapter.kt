package com.example.productcatalog

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ImageView
import android.widget.TextView

class ProductAdapter(context: Context, products: ArrayList<Product>) :
    ArrayAdapter<Product>(context, 0, products) {

    private val inflater = LayoutInflater.from(context)

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view = convertView ?: inflater.inflate(R.layout.item_product, parent, false)
        val product = getItem(position) ?: return view

        view.findViewById<TextView>(R.id.productName).text = product.name
        view.findViewById<TextView>(R.id.productCategory).text = product.category
        view.findViewById<TextView>(R.id.productPrice).text = ProductRepository.formatPrice(product.price)
        ProductImages.show(context, product.image, view.findViewById<ImageView>(R.id.productImage))
        return view
    }
}
