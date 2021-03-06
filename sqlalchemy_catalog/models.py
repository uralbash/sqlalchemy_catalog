#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Model of Pages
"""
# SQLAlchemy
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class Visible(object):
    visible = Column(Boolean)


class BaseProduct2Group(object):
    __tablename__ = 'sacrud_catalog_product2group'

    @declared_attr
    def product_id(cls):
        return Column(
            Integer,
            ForeignKey('sacrud_catalog_product.id'),
            primary_key=True
        )

    @declared_attr
    def group_id(cls):
        return Column(
            Integer,
            ForeignKey('sacrud_catalog_group.id'),
            primary_key=True
        )

    @declared_attr
    def product(cls):
        return relationship(
            "CatalogProduct",
            backref=backref(
                "m2m_product2group",
                cascade="all, delete-orphan"
            )
        )

    @declared_attr
    def group(cls):
        return relationship(
            "CatalogGroup",
            backref=backref(
                "m2m_product2group",
                cascade="all, delete-orphan"
            )
        )


class BaseProduct(Visible):
    """ JSONB parameters

        Example:
            {"size": {"type": "list",
                      "value": (39, 40, 41, 42, 43, 44)
                     },
             "color": {"type": "choice",
                       "value": ("red", "green", "blue", "black", "white")
                       },
             "weight": {"type": "number",
                        "value": "",
                        "metric": "kg"
                        },
            }
    """
    __tablename__ = 'sacrud_catalog_product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    params = Column(JSONB)

    def __repr__(self):
        return self.name


class BaseGroup(Visible):
    __tablename__ = 'sacrud_catalog_group'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # JSON parameters
    params = Column(JSONB)

    # m2m to Product
    @declared_attr
    def products(cls):
        return relationship(
            "CatalogProduct",
            secondary="sacrud_catalog_product2group",
            backref="groups",
        )

    def __repr__(self):
        return self.name


class BaseStock(Visible):
    __tablename__ = 'sacrud_catalog_stock'

    id = Column(Integer, primary_key=True)
    qty = Column(Integer, nullable=False)
    params = Column(JSONB)

    @declared_attr
    def product_id(cls):
        return Column(
            Integer,
            ForeignKey('sacrud_catalog_product.id'),
            nullable=False
        )

    @declared_attr
    def product(cls):
        return relationship(
            "CatalogProduct",
            backref="stock"
        )

    def __repr__(self):
        return "id={}, {}, qty={}".format(self.id, self.product.name, self.qty)
